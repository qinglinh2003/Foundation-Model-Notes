# Lab Experiment Workflow

Standard workflow for implementing lab code, running experiments, writing answers/reports, and updating the appendix. Follow this for every new chapter lab.

---

## Phase 1: Write Experiment Code (Scaffold)

**Location:** `labs/chXX/`

**Files to create:**

| File | Role | Student-facing? |
|------|------|:---:|
| `data.py` | Dataset classes, data loading | Fully provided |
| `model.py` | Model definitions with `# TODO: YOUR CODE HERE` blocks | Student implements TODOs |
| `utils.py` | Training loop, evaluation, plotting, metrics | Fully provided |
| `verify.py` | Sanity checks (shape, mask, consistency) | Fully provided |
| `exp0_*.py` | Experiment 0 script | Fully provided (runs after TODOs filled) |
| `exp1_*.py` | Experiment 1 script | Fully provided |
| `...` | Additional experiments | Fully provided |
| `README.md` | Full lab spec (task, experiments, rubric, pitfalls) | Reference doc |

**Principles:**

- TODOs go in `model.py` only — students implement core architectural logic
- All engineering boilerplate (data loading, training loops, plotting) is provided
- Each experiment script is self-contained: run it and get results
- Every TODO has a detailed comment explaining what to implement
- Scripts should save outputs to `plots/` and `logs/` subdirectories automatically

**Validation:**

```bash
python -m py_compile labs/chXX/*.py
```

All files must pass syntax check.

---

## Phase 2: Fill TODOs and Run Experiments

**Goal:** Produce reference results that demonstrate the lab works correctly.

**Steps:**

1. **Fill TODOs** in `model.py` with correct implementations
2. **Check VPS environment:** `python3 -c "import torch; print(torch.cuda.is_available())"`
3. **Sync to VPS:** use the project rsync pattern
4. **Run in order:**

```bash
cd labs/chXX
python3 verify.py              # sanity checks pass
python3 exp0_*.py              # fastest experiment first
python3 exp1_*.py              # centerpiece experiment
python3 exp2_*.py              # ...
python3 exp3_*.py              # ...
python3 cross_lab_*.py         # last (may depend on other labs)
```

5. **Collect outputs:** plots in `plots/`, CSV logs in `logs/`, stdout captured

**Time estimation:** Before running, estimate time per experiment based on:
- steps × batch_size × model_size
- Previous labs as reference (~1000 steps on tiny model ≈ 2-3 min on RTX 2080 Ti)

---

## Phase 3: Write Answers and Report

**Location:** `labs/chXX/answers/`

**Directory structure:**

```
labs/chXX/answers/
├── report.md                    # Comprehensive report (unified narrative)
├── exp0_*_output.md             # Per-experiment detailed results
├── exp1_*_output.md
├── ...
├── figures/                     # All experiment plots (PNG)
│   ├── exp0_*.png
│   ├── exp1_*.png
│   └── ...
└── logs/                        # Training CSV logs
    ├── exp0_*.csv
    └── ...
```

**Per-experiment output file format:**

```markdown
# Experiment N: [Title]

## Question
What does this experiment test? (1-2 sentences, tied to a chapter section)

## Setup
- Model config (layers, d_model, heads, params)
- Training config (steps, lr, batch_size)
- Conditions compared (A vs B vs C)

## Results

| Config | Val Loss | Key Metric | Observation |
|--------|----------|------------|-------------|
| A      | ...      | ...        | ...         |
| B      | ...      | ...        | ...         |

![Description](figures/expN_*.png)

## Diagnosis
2-3 sentences explaining what the result means. Not just "A is better than B"
but WHY and what it implies for real systems.
```

**Report format (`report.md`):**

```markdown
# Lab X Report: [Lab Title]

## Question
The overarching question this lab answers (1 paragraph)

## Setup
Shared experimental setup (task, data, base model)

## Experiment 0 — [title]
[Results + core insight]

## Experiment 1 — [title] (centerpiece)
[Results + deeper analysis]

...

## Synthesis
| Property | Load-bearing component | Evidence |
|----------|----------------------|----------|
| ...      | ...                  | Exp N    |

## Cross-lab connections
How findings connect to previous/next labs.
```

---

## Phase 4: Update Appendix

**Location:** `appendices/app_labX.tex`

**Steps:**

1. Create `appendices/app_labX.tex`
2. Add `\input{appendices/app_labX}` to `main.tex` (after `\appendix`, in order)
3. Write LaTeX content following this structure:

```latex
\chapter{Lab X: [Title] --- Experimental Results}
\label{app:labX}

Brief intro paragraph stating the lab's thesis and what experiments verify.

\section{Experiment 0: [Title]}

\paragraph{Question.} ...
\paragraph{Setup.} ...
\paragraph{Results.}

\begin{table}[h] ... \end{table}

\begin{figure}[h]
\includegraphics[width=\textwidth]{labs/chXX/answers/figures/expN_*.png}
\caption{...}
\end{figure}

\paragraph{Core insight.}
Not just "A performed better" but:
- What structural/mathematical reason explains this?
- What does this imply for real systems at scale?
- How does this connect to other experiments or chapters?

\section{Experiment 1: [Title] (Centerpiece)}
... (same format, more depth)

\section{Synthesis}
Summary table + cross-lab narrative arc.
```

**Core insight guidelines:**

Each experiment's "Core insight" paragraph should answer:
1. **Why** did this happen? (mechanism, not just observation)
2. **So what?** (implication for building real models)
3. **Connection** to other experiments or chapters (the thread that ties the curriculum together)

Bad: "Pre-norm achieved lower loss than post-norm."
Good: "Pre-norm stabilizes training because layer normalization before attention keeps the residual stream's scale bounded, preventing gradient explosion in deep stacks. This is the same principle as LSTM's cell state highway (Lab 1) — both create a gradient-friendly path through depth."

4. Compile and verify:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

---

## Checklist (per chapter)

- [ ] `labs/chXX/` scaffold code created
- [ ] `labs/chXX/README.md` with full spec
- [ ] `ch0X.tex` has Lab section describing experiments
- [ ] All `.py` files pass `py_compile`
- [ ] TODOs filled, experiments run on VPS
- [ ] `labs/chXX/answers/` with report + per-experiment outputs + figures + logs
- [ ] `appendices/app_labX.tex` written with core insights
- [ ] `main.tex` includes the appendix
- [ ] PDF compiles with zero overfull hbox
