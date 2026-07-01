# Source Pack: 版本控制与 Git

## Source Boundary

- Course: 计算机教育中缺失的一课
- Unit: 08_版本控制与Git
- Snapshot: local course materials accessed on 2026-06-21
- Scope: commit as snapshot and metadata, working tree / staging area / history
  separation, log / diff / blame / show / bisect, branch / merge / rebase,
  remote fetch / pull / push, revert / reset / restore, and the difference
  between local history and shared history

## Source-To-Unit Notes

- The local course index now places this unit after `07_调试与性能分析` and
  before the later packaging / automation / quality units.
- The existing lesson draft already teaches the main spine that this unit
  needs:
  - Git records project state as a history graph, not as a folder backup.
  - `git add` selects the next snapshot; `git commit` creates a new history
    node.
  - `git log`, `git diff`, `git blame`, and `git show` answer different
    history questions.
  - Branches are movable pointers; merge and rebase change the shape of
    history in different ways.
  - `fetch`, `pull`, and `push` control synchronization with a remote.
  - `restore`, `restore --staged`, `commit --amend`, `revert`, and `bisect`
    belong to different layers of undo / diagnosis.
- This unit has no separate public repository or assignment handout in the
  local materials, so it should stay at the level of command reading, history
  reasoning, conflict handling, and safe undo.

## Teaching Focus For The Page

- Start with the central object: a commit as a snapshot plus metadata plus a
  parent pointer.
- Add the state ledger for working tree, staging area, and committed history so
  the learner can tell where a change lives before running a command.
- Use one short history example to connect `log`, `diff`, `blame`, and `show`
  to different questions.
- Use one branch / merge / rebase example to show how history can fan out and
  come back together.
- Use one remote synchronization example to separate observation (`fetch`) from
  integration (`pull`) and publication (`push`).
- Use one undo / diagnosis example to map the right command to the right layer
  of state.

## Gaps And Boundaries

- Pipes, redirection, shell quoting, and path lookup are already covered by
  unit 01 and should not be re-taught here.
- Debugging methodology, logs, benchmarks, and profiler reading belong to unit
  07 and should only be referenced as a prior habit, not expanded again.
- Packaging, automation, and code-quality workflow belong to later units and
  should not be turned into Git history lessons here.
- This unit should avoid pretending there is a mutable external repository
  contract to inspect; the source boundary is the local course material and the
  learner-facing command behavior of Git itself.
