---
name: academic-manuscript-precheck
description: Review original academic manuscript drafts before submission (PDF, DOCX, Markdown or plain text). Produce a structured, evidence-anchored Chinese or English simulated peer-review report with major/minor issues, methodological and statistical checks, references and reproducibility audit, publication-length audit, and prioritized minimal revisions. Use for 初稿AI评审, 论文预审, 初稿审稿, manuscript pre-review, or initial AI assessment. Do not claim to be an actual journal peer reviewer or invent citations, experiments, statistics, or validation results.
compatibility: Requires a text-capable AI agent; optional Python 3.10+ with python-docx and PyMuPDF for extraction scripts. Does not call an LLM API itself.
metadata:
  version: "1.0.0"
  language: "zh-CN,en"
---

# 论文初稿 AI 预审 / Academic Manuscript Precheck

## Activation
Use when a user asks for **初稿 AI 评审** or a structured pre-submission evaluation of a manuscript. This is a **simulation**, not actual anonymous peer review or proof of scientific validity. The default source is **the user's initial draft**, not a later revised file unless they explicitly request a re-review. If both initial and revision are present, ask which is to be reviewed only if not inferable; never silently substitute the revision for the initial draft.

## Required inputs
- Manuscript (PDF, DOCX, TXT, MD, LaTeX-extracted text, or user-supplied content).
- Optional: field, target journal/conference, article type, reviewer criteria, user page/word limits, language, supplementary files.
- When user omits metadata, infer discipline cautiously, default to neutral reviewer criteria, and declare missing venue/format standards.

## Workflow
1. **Read the full source**, including tables, figure captions, references, and supplementary data available. If PDF, examine relevant rendered pages for figures/tables before criticizing visuals. When text-only extraction omits equations, mark them **not verifiable** rather than assuming errors. Prefer source-reading capabilities of the host agent. Optionally run `scripts/extract_manuscript.py` to produce source blocks with stable `block_id` and page/paragraph locations.
2. Establish an **evidence map**: for each issue, record chapter/section, page if available, block ID, a short exact excerpt, and what evidence is missing. Do not invent page numbers for DOCX; use headings, paragraph/table indices instead.
3. Review against `references/review-checklist.md` and `references/evidence-policy.md`. Assess novelty positioning, question-to-method fit, dataset/provenance/splits/leakage, model reproducibility, baselines and ablations, statistics and metric consistency, claims vs evidence, bibliography validity, visual quality, ethics/disclosure, language, structure and length.
4. Separate **verified textual defects** from **inferences or verification requests**. A suspicious number is not a proven false number. Do not invent citations or claim a dataset was opened unless it was. Current external claims require explicit lookup if tools and permission allow it.
5. Assign prioritized severity: A = credibility-blocking or reproducibility-critical; B = important, improves validity or interpretation; C = clarity/format/length. Avoid more than 10-12 actionable issues unless the manuscript genuinely warrants them. Merge overlapping comments; do not inflate criticism to fill a template.
6. For each issue supply: evidence-anchored location, problem, scientific impact, **minimal** recommended fix. When an experiment is needed, provide a protocol and required metrics, not fabricated outcome values. Clearly identify results that need data collection.
7. Evaluate length with venue limits if provided; if not, provide word/page counts as descriptive only. For this user's usual preference only if invoked/requested: two-column target 6-8 pages; single-column target <=12 pages. Identify safe text repetition cuts before suggesting cutting essential evidence.
8. Fill the report following `assets/review-report-template.md`. Keep comments professional and actionable; avoid formulaic praise, exaggeration, or false certainty. End with 3-5 prioritized repairs and an explicit **AI simulation / not a formal peer review** notice.
9. If the report is represented as JSON matching `assets/review-report-example.json`, run `scripts/verify_review.py --source ... --review ...`; resolve invalid excerpt anchors before delivery. The verifier checks text anchoring, not scientific truth. `scripts/render_review.py` can format validated JSON into Markdown.

## Core rules
- **No fabricated experiments, p-values, approval status, reviewer identities, or bibliography.**
- Do not turn potential weaknesses into confirmed factual errors without source evidence.
- Do not claim 100% reviewer acceptance, guaranteed publication, or exact AI-detection percentage.
- Clearly distinguish review of the initial draft from post-revision validation.
- Section-location fidelity outranks report length. Quote excerpts briefly, never replace evidence with imagined passages.
- Offer revision planning only; do not silently rewrite the manuscript when the user asked for a review.
- Respect unpublished manuscript confidentiality; avoid uploading content to public GitHub or third-party systems without explicit approval.
- Provide feedback in user's language by default, with optional bilingual response.

## Bundled resources
- `references/review-checklist.md`: review dimensions and severity anchors.
- `references/evidence-policy.md`: evidence grounding, statistical and citation standards.
- `assets/review-report-template.md`: report layout.
- `assets/review-report-example.json`: JSON output schema example using fictional text only.
- `scripts/extract_manuscript.py`: offline source-to-block JSON extractor.
- `scripts/verify_review.py`: verifies evidence quotes against source blocks.
- `scripts/render_review.py`: turns reviewed JSON into a readable Markdown report.
