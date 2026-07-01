# Source Pack: Toolformer 与自监督工具学习

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: Toolformer 与自监督工具学习
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- Main source: [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) and the corresponding arXiv PDF.
- Public facts used here:
  - Toolformer trains a model to decide which APIs to call, when to call them, what arguments to pass, and how to use the results in future token prediction.
  - Training is self-supervised and requires only a handful of demonstrations for each API.
  - Candidate calls are kept only when the executed tool result lowers future-token loss enough to clear the filter.
  - The public paper examples cover calculator, Q&A, search engines, translation, and calendar.
  - The paper frames calls as text sequences with special markers, so the training data can stay in the language-model format.
- Course bridge:
  - 03 ReAct explains how to read interleaved thought/action/observation traces.
  - 04 turns the same tool-use problem into data generation and loss-based filtering.
  - 05 moves into multi-step tool evaluation.
  - 06 moves into environment interaction and reward-based training.

## Unit Boundary

- Focus: text-sequence API representation, candidate-call sampling, execution and filtering, and the self-supervised finetuning loop.
- Defer: chained tool use, interactive browsing/refinement, sandbox and permission mechanics, benchmark evaluator internals, and environment-RL implementation details.

## Gaps

- No private repository, adapter layer, or internal experiment log is bound to this page.
- Exact hyperparameters and appendix details are intentionally out of scope here; the page teaches the public paper-level mechanism and the course bridge.
