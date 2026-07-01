# Source Pack: ToolBench / API-Bank 与任务评测

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: ToolBench / API-Bank 与任务评测
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- Main public sources:
  - [ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs](https://arxiv.org/abs/2307.16789)
  - [API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs](https://arxiv.org/abs/2304.08244)
  - [StableToolBench: Towards Stable Large-Scale Benchmarking on Tool Learning of Large Language Models](https://arxiv.org/abs/2403.07714)
- Public facts used here:
  - ToolLLM introduces ToolBench as a tool-use framework that combines data construction, training, and evaluation across a large API inventory.
  - API-Bank evaluates tool-augmented LLMs with runnable tasks, planning/retrieval/calling steps, and a separate training set.
  - StableToolBench responds to unstable online APIs by introducing a virtual API server, caching, API simulators, and a more stable evaluator.
  - Tool-use evaluation needs more than text similarity: it has to inspect planning, API selection, argument correctness, execution success, and end-to-end task completion.
  - The benchmark choice changes what the model is rewarded for, so the page keeps benchmark design, metrics, and failure modes together.
- Course bridge:
  - 04 explains how Toolformer creates tool-use training data by filtering candidate calls.
  - This unit explains how multi-step tool tasks are evaluated after the model has learned to call tools.
  - 06 moves from benchmark evaluation into environment interaction and reward-based training.

## Unit Boundary

- Focus: benchmark design, task decomposition, API inventory, metric reading, stability issues, and why evaluation must inspect planning plus execution.
- Defer: environment-RL implementation details, production sandboxing, and private benchmark scripts or repositories.

## Gaps

- No private repository, leaderboard snapshot, or internal benchmark harness is bound to this page.
- Exact online API status and leaderboard numbers drift over time, so future editors should re-check the current arXiv pages or project docs before turning these notes into operational instructions.
