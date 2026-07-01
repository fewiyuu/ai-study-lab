# Source Pack: 沙盒副作用与上线评测

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: 沙盒副作用与上线评测
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- Main public sources:
  - [OpenEnv Integration for Training LLMs with Environments](https://huggingface.co/docs/trl/openenv)
  - [GRPO Trainer](https://huggingface.co/docs/trl/grpo_trainer)
  - [Dataset formats and types](https://huggingface.co/docs/trl/dataset_formats)
  - [Examples](https://huggingface.co/docs/trl/example_overview)
  - [Asynchronous GRPO](https://huggingface.co/docs/trl/async_grpo_trainer) for the later pickling note
- Public facts used here:
  - `environment_factory` lets the trainer orchestrate a stateful tool loop.
  - Environment methods become callable tools during generation.
  - `reset` should clear episode-scoped state before a new run starts.
  - `reward_func` should read from environment state rather than only from surface text.
  - `prompt-only` data is the base shape; environment training differs from prompt-completion and preference formats.
  - In async GRPO, rollout workers run in separate processes, so worker-visible components must be picklable.
  - The public OpenEnv guide and notebook examples provide the factual base; this unit reuses those facts but reorients them toward sandbox side effects and launch gating.

## Course Bridge

- 05 covers benchmark design and task evaluation.
- 06 explains why SFT stops short when the task is stateful.
- 07 turns that boundary into a concrete TRL OpenEnv training loop.
- 08 narrows the same loop to sandbox side effects, approval, audit, rollback, and launch-side evaluation.

## Unit Boundary

- Focus on the difference between sandboxed side effects and live launch risk.
- Focus on the launch gate: allowed actions, audit state, rollback state, and stop conditions.
- Focus on how the same environment state that supports training also feeds evaluation.
- Defer async rollout scaling, distributed worker orchestration, and deeper IAM design to later work.

## Gaps

- TRL public docs and example names can drift; recheck the current docs before turning these notes into operational instructions.
- This pack is a teaching snapshot, not a substitute for the live docs.
