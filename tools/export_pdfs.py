#!/usr/bin/env python3
"""Build a browsable PDF preview package.

The script compiles ``main.tex``, copies the full PDF into ``dist/``,
splits chapter-level entries into separate PDFs, and writes a static
``index.html`` that previews PDFs in the browser.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CHAPTERS_DIR = DIST / "chapters"
MAIN_TEX = ROOT / "main.tex"
MAIN_PDF = ROOT / "main.pdf"
MAIN_TOC = ROOT / "main.toc"
FULL_PDF_NAME = "Foundation-Model-Notes-full.pdf"


@dataclass
class TocEntry:
    title: str
    label: str
    anchor: str
    page_index: int
    output_name: str


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def build_pdf() -> None:
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", str(MAIN_TEX.name)])


def tex_to_text(value: str) -> str:
    value = re.sub(r"\\numberline\s*\{[^}]*\}", "", value)
    value = value.replace(r"\hspace {1em}", " ")
    value = value.replace(r"\&", "&")
    value = value.replace(r"---", "-")
    value = value.replace(r"--", "-")
    value = re.sub(r"\\[a-zA-Z]+\s*", "", value)
    value = value.replace("{", "").replace("}", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "section"


def parse_toc_chapters() -> list[tuple[str, str, str]]:
    text = MAIN_TOC.read_text(encoding="utf-8")
    pattern = re.compile(
        r"\\contentsline \{chapter\}\{(?P<title>.*?)\}\{(?P<label>.*?)\}\{(?P<anchor>.*?)\}%",
        re.DOTALL,
    )
    entries: list[tuple[str, str, str]] = []
    for match in pattern.finditer(text):
        title = tex_to_text(match.group("title"))
        label = tex_to_text(match.group("label"))
        anchor = match.group("anchor").strip()
        if not title or title == "Bibliography":
            continue
        entries.append((title, label, anchor))
    return entries


def make_page_label_map(reader: PdfReader) -> dict[str, int]:
    labels = list(reader.page_labels)
    label_map: dict[str, int] = {}
    for index, label in enumerate(labels):
        label_map.setdefault(str(label), index)
    return label_map


def numbered_output_name(order: int, title: str, anchor: str) -> str:
    prefix = f"{order:02d}"
    chapter_match = re.match(r"chapter\.([0-9A-Za-z]+)$", anchor)
    if chapter_match:
        prefix = f"ch{chapter_match.group(1).lower()}"
    return f"{prefix}-{slugify(title)}.pdf"


def collect_entries(reader: PdfReader) -> list[TocEntry]:
    label_map = make_page_label_map(reader)
    entries: list[TocEntry] = []
    for order, (title, label, anchor) in enumerate(parse_toc_chapters(), start=1):
        if label not in label_map:
            print(f"Skipping {title!r}: page label {label!r} not found")
            continue
        entries.append(
            TocEntry(
                title=title,
                label=label,
                anchor=anchor,
                page_index=label_map[label],
                output_name=numbered_output_name(order, title, anchor),
            )
        )
    entries.sort(key=lambda item: item.page_index)
    return entries


def write_pdf_range(reader: PdfReader, start: int, end_exclusive: int, path: Path) -> None:
    writer = PdfWriter()
    for page_index in range(start, end_exclusive):
        writer.add_page(reader.pages[page_index])
    with path.open("wb") as handle:
        writer.write(handle)


def write_demo_page() -> None:
    demo_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project 1 MiniGPT Demo</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    :root {
      --bg: #0f1117;
      --panel: #1a1d27;
      --panel-2: #232733;
      --text: #e4e7ec;
      --muted: #8b92a5;
      --line: #2a2e3a;
      --accent: #2D8CFF;
      --accent-2: #1A6FD1;
      --accent-dim: rgba(45, 140, 255, 0.12);
      --danger: #ef4444;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
      font-size: 14px;
      line-height: 1.5;
    }
    .demo {
      max-width: 1180px;
      margin: 0 auto;
      padding: 28px;
      display: grid;
      grid-template-columns: minmax(320px, 420px) 1fr;
      gap: 18px;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    .controls { padding: 20px; }
    h1 {
      font-size: 21px;
      line-height: 1.2;
      margin: 0 0 4px;
      letter-spacing: 0;
    }
    .subtitle { color: var(--muted); font-size: 13px; margin-bottom: 18px; }
    label {
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
      margin: 16px 0 6px;
    }
    textarea {
      width: 100%;
      min-height: 140px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #12151d;
      color: var(--text);
      padding: 12px;
      font: inherit;
      outline: none;
    }
    textarea:focus, input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-dim);
    }
    .preset-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }
    .preset, button {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel-2);
      color: var(--text);
      padding: 8px 10px;
      font: inherit;
      cursor: pointer;
    }
    .preset:hover, button:hover { border-color: #3d4255; background: #2b303d; }
    .slider-row {
      display: grid;
      grid-template-columns: 1fr 58px;
      gap: 10px;
      align-items: center;
    }
    input[type="range"] { width: 100%; accent-color: var(--accent); }
    input[type="number"] {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #12151d;
      color: var(--text);
      padding: 7px 8px;
      font: inherit;
    }
    .primary {
      width: 100%;
      margin-top: 20px;
      border-color: var(--accent);
      background: var(--accent);
      color: #fff;
      font-weight: 700;
      padding: 11px 14px;
    }
    .primary:hover { background: var(--accent-2); border-color: var(--accent-2); }
    .primary:disabled { opacity: 0.55; cursor: wait; }
    .meta {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin-top: 18px;
    }
    .metric {
      background: #12151d;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
    }
    .metric span { display: block; color: var(--muted); font-size: 11px; }
    .metric strong { display: block; margin-top: 2px; font-size: 13px; }
    .output {
      min-height: calc(100vh - 56px);
      display: flex;
      flex-direction: column;
    }
    .output-head {
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
    }
    .output-title { font-weight: 700; }
    .status { color: var(--muted); font-size: 12px; }
    pre {
      margin: 0;
      padding: 22px;
      white-space: pre-wrap;
      word-break: break-word;
      font: 15px/1.7 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      color: #f0f3f8;
      flex: 1;
    }
    .placeholder { color: var(--muted); }
    .error { color: var(--danger); }
    @media (max-width: 900px) {
      .demo { grid-template-columns: 1fr; padding: 16px; }
      .output { min-height: 420px; }
    }
  </style>
</head>
<body>
  <div class="demo">
    <section class="panel controls">
      <h1>Project 1 MiniGPT</h1>
      <div class="subtitle">3.7M parameters · Gutenberg corpus · 10K training steps</div>

      <label for="prompt">Prompt</label>
      <textarea id="prompt">The old man</textarea>
      <div class="preset-row">
        <button class="preset" data-prompt="The old man">The old man</button>
        <button class="preset" data-prompt="In the beginning">In the beginning</button>
        <button class="preset" data-prompt="She opened the door">She opened the door</button>
        <button class="preset" data-prompt="The city of Paris">The city of Paris</button>
      </div>

      <label for="temperature">Temperature</label>
      <div class="slider-row">
        <input id="temperature" type="range" min="0.2" max="1.4" step="0.1" value="0.8">
        <input id="temperatureValue" type="number" min="0.2" max="1.4" step="0.1" value="0.8">
      </div>

      <label for="topK">Top-k</label>
      <div class="slider-row">
        <input id="topK" type="range" min="1" max="100" step="1" value="40">
        <input id="topKValue" type="number" min="1" max="100" step="1" value="40">
      </div>

      <label for="maxTokens">Max new tokens</label>
      <div class="slider-row">
        <input id="maxTokens" type="range" min="20" max="240" step="10" value="120">
        <input id="maxTokensValue" type="number" min="20" max="240" step="10" value="120">
      </div>

      <button id="generate" class="primary">Generate</button>

      <div class="meta">
        <div class="metric"><span>Validation loss</span><strong>3.15</strong></div>
        <div class="metric"><span>Bits per byte</span><strong>1.51</strong></div>
        <div class="metric"><span>Context length</span><strong>256 tokens</strong></div>
        <div class="metric"><span>Tokenizer</span><strong>BPE · V=2000</strong></div>
      </div>
    </section>

    <section class="panel output">
      <div class="output-head">
        <div class="output-title">Generated Text</div>
        <div id="status" class="status">Ready</div>
      </div>
      <pre id="output" class="placeholder">Choose a prompt and generate a continuation.</pre>
    </section>
  </div>

  <script>
    const promptEl = document.getElementById('prompt');
    const outputEl = document.getElementById('output');
    const statusEl = document.getElementById('status');
    const button = document.getElementById('generate');

    function bindPair(rangeId, numberId) {
      const range = document.getElementById(rangeId);
      const number = document.getElementById(numberId);
      range.addEventListener('input', () => number.value = range.value);
      number.addEventListener('input', () => range.value = number.value);
    }
    bindPair('temperature', 'temperatureValue');
    bindPair('topK', 'topKValue');
    bindPair('maxTokens', 'maxTokensValue');

    document.querySelectorAll('.preset').forEach((preset) => {
      preset.addEventListener('click', () => {
        promptEl.value = preset.dataset.prompt;
        promptEl.focus();
      });
    });

    button.addEventListener('click', async () => {
      const payload = {
        prompt: promptEl.value,
        temperature: Number(document.getElementById('temperature').value),
        top_k: Number(document.getElementById('topK').value),
        max_tokens: Number(document.getElementById('maxTokens').value),
      };
      button.disabled = true;
      statusEl.textContent = 'Generating...';
      outputEl.className = 'placeholder';
      outputEl.textContent = 'Loading model and sampling tokens...';
      try {
        const response = await fetch('api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Generation failed');
        outputEl.className = '';
        outputEl.textContent = data.text;
        statusEl.textContent = `${data.generated_tokens} tokens · ${data.elapsed_sec.toFixed(2)}s`;
      } catch (error) {
        outputEl.className = 'error';
        outputEl.textContent = error.message;
        statusEl.textContent = 'Error';
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>
"""
    (DIST / "demo.html").write_text(demo_html, encoding="utf-8")


def export_pdfs() -> list[TocEntry]:
    if DIST.exists():
        shutil.rmtree(DIST)
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(MAIN_PDF, DIST / FULL_PDF_NAME)
    cover_src = ROOT / "figures" / "cover" / "cover-landscape.png"
    if cover_src.exists():
        shutil.copy2(cover_src, DIST / "cover.png")
    reader = PdfReader(str(MAIN_PDF))
    entries = collect_entries(reader)
    for index, entry in enumerate(entries):
        next_start = entries[index + 1].page_index if index + 1 < len(entries) else len(reader.pages)
        write_pdf_range(reader, entry.page_index, next_start, CHAPTERS_DIR / entry.output_name)
    return entries


def write_index(entries: list[TocEntry]) -> None:
    complete_chapters = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}
    complete_labs = {1, 2, 3, 4, 5}
    complete_projects = {1}
    front_titles = {"Course Overview", "Course Structure", "Study Schedule"}
    part_labels = [
        (range(1, 6), "Part I — Transformer Foundations"),
        (range(6, 11), "Part II — Engineering Pretraining at Scale"),
        (range(11, 18), "Part III — Post-Training"),
        (range(18, 22), "Part IV — World Models and Model-Based Agents"),
        (range(22, 28), "Part V — Evaluation, VLMs, Serving, Long Context, and Intervention"),
        (range(28, 29), "Part VI — Research Capstone"),
    ]

    def chapter_number(entry: TocEntry) -> int | None:
        match = re.match(r"chapter\.([0-9]+)$", entry.anchor)
        return int(match.group(1)) if match else None

    def item_button(
        entry: TocEntry,
        icon: str,
        icon_class: str,
        status: str | None = None,
        title: str | None = None,
    ) -> str:
        pdf_path = f"chapters/{entry.output_name}"
        status_html = ""
        if status == "complete":
            status_html = '<span class="status-dot status-complete"></span>Complete &middot; '
        elif status == "placeholder":
            status_html = '<span class="status-dot status-placeholder"></span>Placeholder &middot; '
        return (
            f'<button class="item" data-pdf="{html.escape(pdf_path)}">'
            f'<div class="icon {icon_class}">{html.escape(icon)}</div>'
            '<div class="item-text">'
            f'<div class="item-title">{html.escape(title or entry.title)}</div>'
            f'<div class="item-meta">{status_html}p. {html.escape(entry.label)}</div>'
            "</div></button>"
        )

    sidebar_parts: list[str] = []
    total_pages = len(PdfReader(str(MAIN_PDF)).pages)
    sidebar_parts.append(
        '<div class="section-label">Full Book</div>'
        f'<button class="item active" data-pdf="{html.escape(FULL_PDF_NAME)}">'
        '<div class="icon icon-full">ALL</div>'
        '<div class="item-text"><div class="item-title">Complete Book</div>'
        f'<div class="item-meta">{total_pages} pages &middot; All chapters</div>'
        "</div></button>"
    )

    sidebar_parts.append(
        '<div class="section-label">Interactive</div>'
        '<button class="item" data-pdf="demo.html">'
        '<div class="icon icon-demo">GPT</div>'
        '<div class="item-text"><div class="item-title">Project 1 MiniGPT Demo</div>'
        '<div class="item-meta"><span class="status-dot status-complete"></span>Live generation</div>'
        "</div></button>"
    )

    main_entries = [entry for entry in entries if chapter_number(entry) is not None]
    for chapter_range, label in part_labels:
        buttons = []
        for entry in main_entries:
            number = chapter_number(entry)
            if number not in chapter_range:
                continue
            status = "complete" if number in complete_chapters else "placeholder"
            icon_class = "icon-chapter" if status == "complete" else "icon-chapter placeholder"
            buttons.append(item_button(entry, str(number), icon_class, status=status))
        if buttons:
            sidebar_parts.append(f'<div class="section-label">{html.escape(label)}</div>{"".join(buttons)}')

    # --- Projects (specs only, sorted by project number) ---
    project_items: list[tuple[int, str]] = []
    for entry in entries:
        if not entry.title.startswith("Project"):
            continue
        # Skip results and guide appendices — they go in separate sections
        if "Results" in entry.title or "Step-by-Step" in entry.title or "Guide" in entry.title:
            continue
        match = re.match(r"Project\s+([0-9]+)", entry.title)
        proj_number = int(match.group(1)) if match else 0
        icon = f"P{proj_number}" if match else "P"
        title = re.sub(r"^Project\s+[0-9]+:\s*", "", entry.title)
        status = "complete" if proj_number in complete_projects else "placeholder"
        project_items.append((proj_number, item_button(entry, icon, "icon-project", status=status, title=title)))
    project_items.sort(key=lambda x: x[0])
    if project_items:
        sidebar_parts.append(f'<div class="section-label">Projects</div>{"".join(btn for _, btn in project_items)}')

    # --- Project Results (appendices) ---
    result_buttons = []
    for entry in entries:
        if not entry.title.startswith("Project"):
            continue
        if "Results" not in entry.title:
            continue
        match = re.match(r"Project\s+([0-9]+)", entry.title)
        proj_number = int(match.group(1)) if match else 0
        status = "complete" if proj_number in complete_projects else "placeholder"
        result_buttons.append(item_button(entry, f"R{proj_number}", "icon-project", status=status))
    if result_buttons:
        sidebar_parts.append(f'<div class="section-label">Project Results</div>{"".join(result_buttons)}')

    # --- Step-by-Step Guides (appendices) ---
    guide_buttons = []
    for entry in entries:
        if not entry.title.startswith("Project"):
            continue
        if "Step-by-Step" not in entry.title and "Guide" not in entry.title:
            continue
        match = re.match(r"Project\s+([0-9]+)", entry.title)
        proj_number = int(match.group(1)) if match else 0
        status = "complete" if proj_number in complete_projects else "placeholder"
        guide_buttons.append(item_button(entry, f"G{proj_number}", "icon-project", status=status))
    if guide_buttons:
        sidebar_parts.append(f'<div class="section-label">Step-by-Step Guides</div>{"".join(guide_buttons)}')

    # --- Lab Results ---
    lab_buttons = []
    for entry in entries:
        if not entry.title.startswith("Lab "):
            continue
        match = re.match(r"Lab\s+([0-9]+)", entry.title)
        lab_number = int(match.group(1)) if match else 0
        status = "complete" if lab_number in complete_labs else "placeholder"
        lab_buttons.append(item_button(entry, f"L{lab_number}", "icon-lab", status=status))
    if lab_buttons:
        sidebar_parts.append(f'<div class="section-label">Lab Results</div>{"".join(lab_buttons)}')

    front_buttons = []
    front_icon = 1
    for entry in entries:
        if entry.title not in front_titles:
            continue
        front_buttons.append(item_button(entry, str(front_icon), "icon-front"))
        front_icon += 1
    if front_buttons:
        sidebar_parts.append(f'<div class="section-label">Front Matter</div>{"".join(front_buttons)}')

    sidebar_html = "\n".join(sidebar_parts)
    progress_pct = round(100 * len(complete_chapters) / max(len(main_entries), 1))
    build_version = str(int((DIST / FULL_PDF_NAME).stat().st_mtime))
    first_pdf_url = f"{FULL_PDF_NAME}?v={build_version}"

    index_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Foundation Model Notes</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
      --bg: #0f1117;
      --panel: #1a1d27;
      --panel-hover: #232733;
      --text: #e4e7ec;
      --muted: #8b92a5;
      --accent: #2D8CFF;
      --accent-dim: rgba(45, 140, 255, 0.12);
      --accent-border: rgba(45, 140, 255, 0.4);
      --line: #2a2e3a;
      --radius: 8px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
      font-size: 14px;
      line-height: 1.5;
    }
    .app {
      display: grid;
      grid-template-columns: 340px 1fr;
      height: 100vh;
    }
    aside {
      background: var(--panel);
      border-right: 1px solid var(--line);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }
    aside::-webkit-scrollbar { width: 6px; }
    aside::-webkit-scrollbar-track { background: transparent; }
    aside::-webkit-scrollbar-thumb { background: var(--line); border-radius: 3px; }
    .sidebar-header {
      padding: 24px 20px 16px;
      border-bottom: 1px solid var(--line);
      position: sticky;
      top: 0;
      background: var(--panel);
      z-index: 10;
    }
    .sidebar-header h1 {
      font-size: 17px;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 4px;
    }
    .sidebar-header .subtitle {
      color: var(--muted);
      font-size: 12px;
    }
    .sidebar-content {
      padding: 12px 12px 24px;
      flex: 1;
    }
    .section-label {
      color: var(--muted);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 16px 8px 6px;
    }
    .item {
      width: 100%;
      border: 1px solid transparent;
      background: transparent;
      color: inherit;
      cursor: pointer;
      text-align: left;
      padding: 10px 12px;
      border-radius: var(--radius);
      display: flex;
      align-items: flex-start;
      gap: 10px;
      transition: all 0.15s ease;
      font-family: inherit;
      font-size: inherit;
    }
    .item:hover { background: var(--panel-hover); }
    .item.active {
      border-color: var(--accent-border);
      background: var(--accent-dim);
    }
    .item .icon {
      flex: 0 0 auto;
      width: 28px;
      height: 28px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 700;
      margin-top: 1px;
    }
    .icon-full { background: var(--accent); color: #fff; }
    .icon-front { background: #6B9FD4; color: #fff; }
    .icon-chapter { background: #2D8CFF; color: #fff; }
    .icon-chapter.placeholder { background: #1a3a5c; color: #5a8ab5; }
    .icon-project { background: #1A6FD1; color: #fff; }
    .icon-lab { background: #5BAAFF; color: #fff; }
    .icon-demo { background: #2D8CFF; color: #fff; }
    .item-text {
      min-width: 0;
      flex: 1;
    }
    .item-title {
      font-size: 13px;
      font-weight: 500;
      line-height: 1.3;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .item-meta {
      color: var(--muted);
      font-size: 11px;
      margin-top: 2px;
    }
    .status-dot {
      display: inline-block;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      margin-right: 4px;
      vertical-align: middle;
    }
    .status-complete { background: #2D8CFF; }
    .status-placeholder { background: #6b7280; }
    main {
      display: flex;
      flex-direction: column;
      min-width: 0;
      background: #262930;
    }
    header {
      background: var(--panel);
      border-bottom: 1px solid var(--line);
      padding: 14px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      justify-content: space-between;
    }
    .header-title {
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-weight: 600;
      font-size: 15px;
    }
    .actions {
      display: flex;
      gap: 8px;
      flex: 0 0 auto;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--panel-hover);
      color: var(--text);
      padding: 8px 14px;
      font-size: 13px;
      font-weight: 500;
      text-decoration: none;
      transition: all 0.15s ease;
      cursor: pointer;
    }
    .btn:hover { background: #2f3340; border-color: #3d4255; }
    .btn-primary {
      border-color: var(--accent);
      background: var(--accent);
      color: #000;
      font-weight: 600;
    }
    .btn-primary:hover { background: #1A6FD1; }
    .btn svg {
      width: 14px;
      height: 14px;
      fill: currentColor;
    }
    iframe {
      flex: 1;
      width: 100%;
      border: 0;
      background: #1e1e1e;
    }
    .progress-bar {
      margin: 12px 8px 0;
      padding: 12px;
      background: rgba(45, 140, 255, 0.08);
      border: 1px solid rgba(45, 140, 255, 0.2);
      border-radius: var(--radius);
    }
    .progress-label {
      font-size: 11px;
      color: var(--muted);
      margin-bottom: 6px;
      font-weight: 500;
    }
    .progress-track {
      height: 4px;
      background: var(--line);
      border-radius: 2px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: #2D8CFF;
      border-radius: 2px;
    }
    .progress-text {
      font-size: 11px;
      color: #2D8CFF;
      margin-top: 4px;
      font-weight: 500;
    }
    @media (max-width: 900px) {
      .app { grid-template-columns: 1fr; grid-template-rows: 45vh 1fr; }
      aside { border-right: 0; border-bottom: 1px solid var(--line); }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside>
      <div class="sidebar-header">
        <img src="cover.png" alt="Cover" style="width:100%;border-radius:8px;margin-bottom:12px;display:block;">
        <h1>Foundation Model Notes</h1>
        <div class="subtitle">Architecture, Training, Alignment &amp; Evaluation</div>
      </div>
      <div class="sidebar-content">
        <div class="progress-bar">
          <div class="progress-label">Content Progress</div>
          <div class="progress-track"><div class="progress-fill" style="width: __PROGRESS_PCT__%"></div></div>
          <div class="progress-text">__COMPLETE_COUNT__ / __TOTAL_CHAPTERS__ chapters complete</div>
        </div>
        __SIDEBAR_HTML__
      </div>
    </aside>
    <main>
      <header>
        <div class="header-title" id="currentTitle">Complete Book</div>
        <div class="actions">
          <a class="btn" id="openLink" href="__FIRST_PDF_URL__" target="_blank" rel="noopener">
            <svg viewBox="0 0 20 20"><path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/></svg>
            Open in new tab
          </a>
          <a class="btn btn-primary" id="downloadLink" href="__FIRST_PDF_URL__" download>
            <svg viewBox="0 0 20 20"><path d="M10 3a1 1 0 011 1v7.586l2.293-2.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 11.586V4a1 1 0 011-1z"/><path d="M3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"/></svg>
            Download
          </a>
        </div>
      </header>
      <iframe id="viewer" src="__FIRST_PDF_URL__"></iframe>
    </main>
  </div>
  <script>
    const viewer = document.getElementById('viewer');
    const currentTitle = document.getElementById('currentTitle');
    const openLink = document.getElementById('openLink');
    const downloadLink = document.getElementById('downloadLink');
    const buildVersion = '__BUILD_VERSION__';
    function versioned(path) {
      return path + '?v=' + buildVersion;
    }
    document.querySelectorAll('.item').forEach(function(button) {
      button.addEventListener('click', function() {
        document.querySelectorAll('.item').forEach(function(item) { item.classList.remove('active'); });
        button.classList.add('active');
        var pdf = button.dataset.pdf;
        var title = button.querySelector('.item-title').textContent;
        var pdfUrl = versioned(pdf);
        viewer.src = pdfUrl;
        currentTitle.textContent = title;
        openLink.href = pdfUrl;
        downloadLink.href = pdfUrl;
      });
    });
  </script>
</body>
</html>
"""
    index_html = (
        index_html.replace("__SIDEBAR_HTML__", sidebar_html)
        .replace("__PROGRESS_PCT__", str(progress_pct))
        .replace("__COMPLETE_COUNT__", str(len(complete_chapters)))
        .replace("__TOTAL_CHAPTERS__", str(len(main_entries)))
        .replace("__FIRST_PDF_URL__", html.escape(first_pdf_url))
        .replace("__BUILD_VERSION__", html.escape(build_version))
    )
    (DIST / "index.html").write_text(index_html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-build", action="store_true", help="Reuse existing main.pdf/main.toc")
    args = parser.parse_args()

    if not args.no_build:
        build_pdf()
    if not MAIN_PDF.exists() or not MAIN_TOC.exists():
        raise SystemExit("main.pdf and main.toc must exist. Run without --no-build first.")
    entries = export_pdfs()
    write_demo_page()
    write_index(entries)
    print(f"\nWrote preview package: {DIST}")
    print(f"Open locally: {DIST / 'index.html'}")
    print("Serve locally: python3 -m http.server 8080 -d dist")


if __name__ == "__main__":
    main()
