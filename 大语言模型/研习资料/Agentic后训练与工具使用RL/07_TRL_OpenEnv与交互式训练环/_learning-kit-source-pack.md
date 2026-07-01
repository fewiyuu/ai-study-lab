# Source Pack: TRL OpenEnv 与交互式训练环

## Source Boundary

- Course: Agentic 后训练与工具使用 RL
- Unit: TRL OpenEnv 与交互式训练环
- Snapshot: access date 2026-06-21

## Source-To-Unit Notes

- Main public sources:
  - [OpenEnv Integration for Training LLMs with Environments](https://huggingface.co/docs/trl/openenv)
  - [GRPO Trainer](https://huggingface.co/docs/trl/grpo_trainer)
  - [Dataset formats and types](https://huggingface.co/docs/trl/dataset_formats)
  - [Examples](https://huggingface.co/docs/trl/example_overview)
  - [Asynchronous GRPO](https://huggingface.co/docs/trl/async_grpo_trainer) for the later pickling note
- Public facts used here:
  - TRL’s `GRPOTrainer` supports interactive environment training through `environment_factory`.
  - When `environment_factory` is provided, the trainer handles the multi-turn tool-calling loop: generate, parse tool calls, execute tools, and feed results back into the model.
  - `environment_factory` is the recommended path when the environment owns the stateful interaction and the trainer should orchestrate the loop.
  - `rollout_func` is the lower-level alternative when an external server or custom protocol must own generation and interaction.
  - The migration map from `rollout_func` to `environment_factory` is part of the official OpenEnv guide.
  - GRPO training is anchored in prompt-only data; dataset shape differs from prompt-completion and preference training.
  - Public methods on the environment class become tools for the model to call during generation.
  - In the async GRPO path, rollout workers run in a separate process, so `reward_funcs`, `tools`, and `environment_factory` must be picklable.
  - When a reward function is not applicable to a sample, `None` can be used so that the reward is excluded for that sample.
  - TRL examples include OpenEnv notebooks for Wordle and Sudoku, plus a BrowserGym notebook that uses the lower-level `rollout_func` path.

## Course Bridge

- 05 focuses on benchmark design and task evaluation: what to measure after a model already calls tools.
- 06 explains when SFT is no longer enough and the task needs a stateful environment plus rewards.
- 07 turns that boundary into a concrete TRL OpenEnv training loop and reads like an implementation bridge.
- 08 narrows the same loop to sandbox side effects, approval, and launch-side evaluation.

## Unit Boundary

- Focus on the decision boundary between stateless tools and stateful environments.
- Focus on `environment_factory`, `reset`, tool methods, `reward_func`, and `max_completion_length`.
- Focus on how environment state becomes reward, and how trainer-managed interaction differs from a custom rollout loop.
- Defer sandbox policy, production approvals, and async rollout scaling details to later units.

## Gaps

- Exact TRL API details and notebook names can drift over time; future editors should re-check the current public docs before turning these notes into operational steps.
- This page uses public docs as the factual base and the course sequence as the teaching scaffold.
