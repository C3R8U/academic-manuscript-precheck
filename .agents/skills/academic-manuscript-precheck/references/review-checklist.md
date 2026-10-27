# Manuscript pre-review checklist

## A. Topic and contribution
- Is the question identifiable and the scientific contribution distinguishable from prior work?
- Are novelty statements restrained to what was demonstrated?
- Does title/abstract accurately represent the actual methodology and output (e.g. 2D versus 3D)?

## B. Sources, data and leakage
- Is dataset/source, license, version, sample size, collection, filtering and label definition clear?
- Are samples independent? Same entity, patient, scene or author cannot appear across train/test if testing independent generalization.
- Are split strategy, stratification, class balance, duplicates, annotation consensus, and missing data described?
- Are publicly accessible data and code claims backed by a working repository with the promised contents?

## C. Methods and reproducibility
- Are formulas dimensionally and semantically consistent and defined once?
- Are backbone, training/validation/test protocols, seeds, hardware, stopping, hyperparameters specified?
- Do method assumptions match input format and labels? Are claims of 'adaptive' or 'causal' actually supported?
- Are preprocessing transformations fitted only on training data?

## D. Results and interpretation
- Does every central claim have a table, figure, derivation, or reference directly supporting it?
- Are independent baselines comparable in training data, budget and measurement methodology?
- Are ablations capable of isolating the named component and avoid test-set tuning?
- Are confidence intervals, SD or statistical comparisons relevant and correctly interpreted?
- Are metrics compatible with each other and the task (macro/micro metrics, image-level vs scene-level)?
- Are unseen-category and unseen-style tests distinguished; is external generalization supported?

## E. Paper communication
- Do section roles differ (methods: what/how; results: numbers; discussion: meaning/limits; conclusion: brief synthesis)?
- Are tables, images, equation numbering and citations coherent and not redundant?
- Is the page length appropriate for the target venue? Shorten repetitive narrative before essential experiments.
- Are source and code availability statements accurate, not aspirational claims represented as achieved?

## F. Research ethics
- Check privacy, consent, license terms, human-subject approval where applicable.
- Note missing AI assistance disclosure only when the publication venue requires it or user requests compliance audit.

## Five-category scoring guide (optional; not an official venue standard)
Weights: contribution/positioning 20; methodological rigor 25; evidence sufficiency 25; coherence 15; writing & reporting 15. Each dimension score 1-5. Weighted score / 5 converted to 100 is explanatory only, not acceptance probability.

Severity:
- A: a central conclusion is unsupported; reproducibility impossible in a crucial step; leakage; fatal mismatch in task or metric.
- B: needed controls, clarifications, uncertainty or comparative evidence; moderate reporting inaccuracies.
- C: layout, repetition, nomenclature, imprecise wording, noncritical citation formatting.

Conclude with one of: substantial revision recommended / targeted revision recommended / suitable for professional review after minor polishing; not an acceptance/rejection decision.
