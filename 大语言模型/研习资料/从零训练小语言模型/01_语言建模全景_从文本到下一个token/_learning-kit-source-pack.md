# Source Pack: 语言建模全景：从文本到下一个 token

## Source Boundary

- Course: 从零训练小语言模型
- Unit: 01 语言建模全景：从文本到下一个 token
- Snapshot: 2026-06-21
- Access date: 2026-06-21
- Local inputs: course-root `index.html` and the existing unit page `学习页.html` for the same unit.

## Source-To-Unit Notes

- `index.html` fixes the course placement, phase order, and the fact that this unit is the foundation for later tokenizer, Transformer, training, system, and evaluation units.
- The existing unit page provides the anchor lesson shape: text -> token -> logits -> loss -> parameter update, plus the public reference names already exposed to the learner.
- Public reference names already visible in the existing page copy: Stanford CS336: Language Modeling from Scratch, `llm.c`, OLMo 2 technical report, and the OLMo project page. Keep them as source labels only; do not expand beyond what the existing page already supports.
- This rewrite should keep the unit at the objective/loss-loop level and leave tokenizer internals, Transformer internals, optimization details, GPU performance, scaling, and full open-training recipes to later units.

## Gaps

- No local transcript, paper excerpt, or repository snapshot was provided for deeper claims, so do not invent extra details about CS336, `llm.c`, or OLMo 2.
- Do not promote the unit into an implementation lesson for tokenizer internals or training system details; this page is only the training-objective entry point.
- If later unit pages need stronger operational details, add a new source pack for that unit instead of stretching this one.
