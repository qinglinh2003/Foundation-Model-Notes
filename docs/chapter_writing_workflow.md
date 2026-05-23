# Chapter Writing Workflow

Reusable workflow for writing a new chapter from scratch. Distilled from ch10-ch12 production experience.

---

## Operating Principle

The chapter workflow is a two-agent loop:

- **Primary writer** drafts the full chapter in one voice.
- **Reviewer** audits structure, technical calibration, style consistency, figures, compilation, and deployment.

Do not split first-draft sections between agents unless the user explicitly asks for parallel drafting. Split drafting tends to produce inconsistent narrative voice. Parallel work is better used for review, prompt writing, figure mapping, and deployment checks.

A chapter is not "done" when the tex compiles. It is done when:

1. The chapter matches the book's established style and pedagogy.
2. Figure prompts exist and are self-contained.
3. Final generated images are integrated.
4. `main.pdf` and per-chapter PDFs compile.
5. The website preview is deployed.
6. The chapter is marked complete in the preview UI.

## Phase 1: Design (discussion round)

**Goal**: Lock down what the chapter should teach, its internal structure, and how it connects to neighboring chapters.

1. **Position the chapter**: What does the reader know coming in (prior chapter)? What do they lack? What must they know before the next chapter?
2. **Identify the chapter's core thesis**: One sentence that the entire chapter proves. Every section should serve this thesis.
3. **Draft section outline**: Section-by-section plan with ~page estimates, key elements per section (figures, boxes, equations, exercises).
4. **Settle design decisions**: Resolve any open questions (ordering, scope, depth) via agent discussion before writing.

Deliverable: A locked section outline with page budget and element inventory.

---

## Phase 2: Writing (single-agent draft)

**Goal**: One agent writes the complete chapter; the other reviews.

### Conventions to follow (from Part II/III established pattern)

**Front matter** (in order):
- Opening hook: a concrete, surprising anecdote (who did what, when, why is it surprising). NOT a bridge sentence.
- Bridge paragraph: connects to prior chapter/part.
- Chapter thesis statement.
- `\begin{learningobjectives}` environment (4-6 items)
- Notation table (`\begin{tabular}`) if the chapter introduces new symbols
- Timeline table (7-8 rows max, covering the chapter's key contributions chronologically)
- "What this chapter covers" paragraph — narrative promise, not a table of contents. Use a three-beat or question-form structure.

**Section body**:
- Every section ends with `\begin{quickrecap}` including an italic `\textit{Next:}` transition sentence
- Use `\subsection{}` liberally for sections covering 2+ distinct subtopics (aim for 2-3 subsections per long section)
- Project callouts: `\begin{tcolorbox}[colback=orange!5, colframe=orange!60, title=\textbf{For Project~N: ...}]` with bulleted items
- Conceptual debate/discussion: blue `\begin{tcolorbox}[colback=blue!5, colframe=blue!40, title=...]`
- Cross-chapter echo: gray `\begin{tcolorbox}[colback=gray!8, colframe=gray!40]` connecting current lesson to a prior chapter's established lesson
- Pause-and-verify: `\begin{mdframed}[style=intuitioncheck]` with a concrete calculation or thought experiment (2 per chapter)
- Figures: `\begin{figure}[t]` with descriptive `\caption{}` and `\label{fig:...}`

**End matter** (in order):
- `\begin{takeaways}` environment (5-7 items)
- `\section*{Summary}` with:
  - "What this chapter established" paragraph
  - Chapter-specific meta-lesson paragraph (named — e.g., "The data-as-algorithm lesson", "The low-rank insight")
  - "One sentence" distillation
  - "What comes next" forward reference
- `\section*{Key Equations}` — 2-4 equations with one-line descriptions
- `\section*{Key Readings}` — 5-7 papers, each with a one-sentence annotation

**Formatting**:
- `\raggedbottom` at chapter start, `\flushbottom` at chapter end
- Running example (Project model) threaded through every section
- Figure density: ~1 figure per 3-4 pages (8 figures for a 30-page chapter, 5 for a 17-page chapter)

### Writing rules
- One agent writes the full chapter in one pass (don't split sections between agents — voice will fragment)
- Add all bib entries needed
- Create placeholder PNGs in `figures/chNN/` so the book compiles
- Verify: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` must pass

---

## Phase 3: Style Review (second agent)

**Goal**: Audit the draft against the established conventions of all prior chapters.

Checklist:
- [ ] Opening hook is a concrete anecdote, not a bridge sentence
- [ ] At least one analogy or metaphor grounds an abstract concept
- [ ] Every section ends with quickrecap
- [ ] Long sections have subsections
- [ ] At least 1 blue tcolorbox (conceptual debate)
- [ ] At least 1 gray tcolorbox (cross-chapter echo) if applicable
- [ ] Project callouts use orange tcolorbox, not inline `\paragraph{}`
- [ ] Summary has a named meta-lesson paragraph
- [ ] No "quantify" promises that aren't delivered later
- [ ] Forward references to later sections/chapters are accurate
- [ ] Technical claims are calibrated (not over-strong)
- [ ] No implementation-specific tool names unless the chapter is explicitly about tooling

---

## Phase 4: Content Iteration (user-driven)

**Goal**: Incorporate external review feedback.

1. User provides feedback (or external reviewer feedback).
2. Agents assess each point: valid / partially valid / push back.
3. Make changes, re-compile, verify.
4. Deploy to preview site.

---

## Phase 5: Figure Prompts

**Goal**: Write image generation prompts for GPT Image 2.

### Prompt template

Every prompt file lives in `prompts/chNN/figK_descriptive_name.md` and follows this structure:

```markdown
# Figure NN.K: Title

**Filename**: `fig_descriptive_name.png`
**LaTeX label**: `fig:descriptive-name`
**Caption**: [Full caption text as it appears in the tex file]

## Prompt

\```text
Draw a [specific thing] for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
[1-2 sentences: what this figure teaches and why it matters]

MAIN COMPOSITION:
[Detailed layout description with ALL CAPS subsection headers
for each major visual element. Include specific internal content:
mini-illustrations, textures, icons, labels, numbers.]

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — ONE focal element only
- Text: #1A1A2E (headers), #6B7280 (annotations)
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
[5-8 specific DO NOT constraints]
[Layout constraints: "fill full width", "no empty corners", etc.]
[Readability: "All text readable at 50% PDF width"]
\```

## Review Checklist

- [ ] [8-12 specific visual checks]
```

### Style rules for prompts

1. **Do NOT reference other chapters' figures by name** (e.g., "Match Ch7 Bandwidth Hierarchy"). The image generation model cannot see the textbook. Describe the desired visual style directly instead.
2. **Make every prompt self-contained**: repeat the style system, palette, layout rules, and visual density requirements inside every prompt. Do not assume the image model remembers earlier prompts.
3. **Single orange accent rule**: `#FF9F43` appears on exactly one focal element per figure. Everything else is blue-white.
4. **Rich internal content**: every panel/card/node should contain mini-illustrations (tiny charts, icons, textures, labels), not just text labels in boxes.
5. **Fill the canvas**: landscape figures must use the full width. No large empty regions. If the primary content doesn't fill the space, add annotation strips, consequence panels, or summary banners.
6. **Concrete numbers over abstract labels**: prefer "14 GB" over "large", "128x compression" over "significant reduction".
7. **Consistent hex codes**: always include the full STYLE block with all hex codes, even if it seems repetitive across prompts. The image model needs it every time.
8. **Avoid prompt contradictions**: do not ask for gradients/glow/3D in one line and prohibit them later. Keep the visual instructions internally consistent.

### Prompt naming convention

Files: `prompts/chNN/figK_descriptive_name.md` where K matches the figure number in the chapter.

Figure filenames in tex: `fig_descriptive_name.png`, stored in `figures/chNN/`.

---

## Phase 6: Image Generation and Integration

1. User generates images via GPT Image 2 using the prompts.
2. Images arrive in `figures/chNN/` with ChatGPT timestamp names (e.g., `ChatGPT Image May 23, 2026, 08_41_33 AM.png`).
3. Agent views each image, identifies content, maps to target filename.
4. Agent renames files to match `\includegraphics` references in the tex file.
5. Remove old placeholder PNGs.
6. Compile: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
7. Deploy: `DEPLOY_ROOT=/var/www/qinglinh.com/capstone bash tools/deploy_to_qinglinh_site.sh`
8. Update `complete_chapters` set in `tools/export_pdfs.py` if this is a new chapter going from placeholder to complete.

---

## Phase 7: Deploy

```bash
# Compile
cd /home/qinglinh/Research-OS/vault/projects/Capstone-Curriculum/code && \
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

# Export per-chapter PDFs + index.html
python3 tools/export_pdfs.py

# Deploy to qinglinh.com
DEPLOY_ROOT=/var/www/qinglinh.com/capstone bash tools/deploy_to_qinglinh_site.sh
```

Post-deploy verification:
- Check `https://qinglinh.com/capstone/` returns HTTP 200
- Check the specific chapter PDF URL returns HTTP 200
- Confirm the sidebar shows correct complete/placeholder status
