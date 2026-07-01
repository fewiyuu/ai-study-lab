# Source Pack: 01 本地启动最小 Agent

## Source Boundary

- Course: Claude Code 工作流
- Unit: 01 本地启动最小 Agent
- Snapshot: 2026-06-21
- Source mode: only the local course map and the legacy study-page draft were used; no web crawl.

## Source Summary

- `../index.html`: gives the course position, phase order, and the next unit.
- `学习页.html` in this folder: legacy draft with the concrete operational material for this unit, including the Agent-vs-chat distinction, Quick Start, the three config fields, runtime observation, failure triage, and practice prompts.

## Source-To-Unit Notes

- The course map places this unit in the 01-05 entry phase, so it should establish the first stable intuition and shared vocabulary.
- The legacy draft contains the key operational facts worth preserving: `learn-claude-code`, `s01_agent_loop.py`, `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, and `hello.py`.
- The unit should teach a learner to hand off a task to the model, let local code execute the allowed action, and verify the real side effect on disk or in the shell.

## Unit Boundary

- This page only handles the first local bootstrap of a minimal Agent.
- Message history, tool dispatch, planning, sub-agents, task persistence, permissions, hooks, memory, recovery, scheduling, and MCP belong to later units in the course map.

## Inferred Ordering

- The course map is the source of the phase order; later recommendations are treated as instructional sequencing, not as additional source claims.
- The legacy draft does not provide a public commit hash or repo release, so the operational examples remain exactly as written in the draft and are not expanded into fresh external claims.

## Gaps

- The current local sources are enough to teach this unit, but they do not provide a verified upstream version or a public repository snapshot.
- No external references were added here; this pack is intentionally limited to the two local course files above.
