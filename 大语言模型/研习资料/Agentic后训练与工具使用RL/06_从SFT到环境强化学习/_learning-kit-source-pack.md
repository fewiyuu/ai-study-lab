# Source Pack: 从 SFT 到环境强化学习

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: 从 SFT 到环境强化学习
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- Main public sources:
  - [OpenEnv Integration for Training LLMs with Environments](https://huggingface.co/docs/trl/openenv)
  - [GRPO Trainer](https://huggingface.co/docs/trl/grpo_trainer)
  - [Dataset formats and types](https://huggingface.co/docs/trl/dataset_formats)
  - [Examples](https://huggingface.co/docs/trl/example_overview)
- Public facts used here:
  - OpenEnv provides a standard way to define, deploy, and interact with environments for RL and agentic workflows.
  - OpenEnv environments can run as backend servers, so the model loop is not just text generation; it is a stateful interaction with reset/step-style behavior.
  - GRPOTrainer supports environment-based training through `environment_factory`.
  - In async rollout paths, the rollout worker is a separate process, so tools, reward functions, and `environment_factory` must be picklable.
  - GRPOTrainer supports custom reward functions, including async reward functions when the reward depends on slower I/O.
  - TRL dataset formats distinguish prompt-only data, language modeling data, and other trainer-specific formats; SFT-style training and environment RL do not consume the same supervision shape.
  - OpenEnv notebooks and scripts in TRL show the intended training integration surface for environment-based runs.

## Course Bridge

- 05 focuses on benchmark design and task evaluation: what to measure after a model already calls tools.
- This unit explains when benchmark evidence is not enough and the training loop needs environment feedback instead of only offline supervision.
- 07 turns the same idea into a concrete TRL OpenEnv training loop.
- 08 narrows the same loop to sandboxing, side effects, and上线前评测.

## Unit Boundary

- Focus on the decision boundary between SFT, offline preference-style training, and environment RL.
- Focus on the state that must be tracked in a rollout: observation, action, reward, terminal condition, and episode-level failure modes.
- Focus on why environment isolation, reward design, and picklable factories matter before the trainer can run reliably.
- Defer detailed TRL scripts, sandbox backends, and production approval flow to later units.

## Gaps

- Exact TRL APIs and notebook layout can change; future editors should re-check the current public docs before turning these notes into operational steps.
- This page uses the public docs as its factual base and the course sequence as its teaching scaffold.
