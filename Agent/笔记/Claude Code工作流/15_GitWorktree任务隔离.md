---
title: 15_GitWorktree任务隔离
aliases:
  - Git Worktree任务隔离
  - 任务隔离上GitWorktree
  - Learn Claude Code 15
tags:
  - LearnClaudeCode
  - Git
  - worktree
  - task-isolation
  - learning-kit
source: https://www.bilibili.com/video/BV117DuB8E1M
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. `git worktree` 解决了普通分支切换的什么问题？
> 2. worktree、branch、repo 三者分别是什么？
> 3. 创建新任务 worktree 的最小命令是什么？
> 4. `git worktree list` 能看到什么？
> 5. `git worktree remove` 删除的是目录还是分支？
> 6. 已有分支如何重新挂载成 worktree？
> 7. 为什么 AI coding agent 特别适合用 worktree 做任务隔离？

> [!abstract] 核心主线
> Git Worktree 允许同一个仓库创建多个工作目录，每个目录可以 checkout 不同分支。普通 `git checkout -b` 只能让一个目录在多个分支之间来回切换，同一时刻只能干一个任务；worktree 则能让 `repo/`、`dev-branch-3/`、`dev-branch-4/` 同时存在，各自绑定不同分支。`git worktree add` 用于创建或恢复工作目录，`git worktree list` 用于查看当前 worktree，`git worktree remove` 删除的是工作目录，不会自动删除分支。对 AI coding agent 来说，worktree 把任务隔离到独立目录，避免多个 Agent 共用一个工作区时互相切分支、互相污染文件状态。

## 概念精讲

### 普通分支切换的限制

传统流程是：

```bash
git checkout -b dev-branch-1
# 做任务一
git checkout master
git checkout -b dev-branch-2
# 做任务二
```

这种方式可以创建多个分支，但它们都在同一个工作目录里轮流使用。当前目录同一时刻只能处在一个分支上。

如果任务一改到一半，任务二突然插进来，就会遇到脏工作区、stash、临时提交和切分支冲突等问题。

### Worktree 的直觉

Worktree 是同一个 Git 仓库挂出的多个工作目录。

| 层次 | 直觉 | 例子 |
|---|---|---|
| repo | Git 仓库本体 | `repo/` |
| branch | 一条提交指针 | `dev-branch-3` |
| worktree | 可编辑、可运行的工作目录 | `../dev-branch-3/` |

多个 worktree 共享 Git 对象数据，但每个 worktree 有自己的文件树和当前分支。

## 常用命令

### 创建新分支和新目录

```bash
git worktree add ../dev-branch-3 -b dev-branch-3 master
```

含义：

- `../dev-branch-3`：新工作目录位置。
- `-b dev-branch-3`：创建一个新分支。
- `master`：新分支的起点。

进入新目录后：

```bash
cd ../dev-branch-3
git branch --show-current
```

当前分支就是 `dev-branch-3`。

### 查看 worktree

```bash
git worktree list
```

它会列出当前仓库挂出的所有工作目录，以及每个目录对应的 commit 和 branch。

### 删除 worktree 目录

```bash
git worktree remove ../dev-branch-3
```

这主要删除本地工作目录，不会自动删除 `dev-branch-3` 分支。

> [!warning] remove 不是 delete branch
> `git worktree remove` 删除的是 worktree 目录；如果要删除分支，需要另外使用 `git branch -d branch-name`。

### 恢复已有分支目录

如果 `dev-branch-4` 分支已经存在，不要再用 `-b` 创建同名分支。

```bash
git worktree add ../dev-branch-4 dev-branch-4
```

这表示：把已有 `dev-branch-4` 分支重新挂载成 `../dev-branch-4` 工作目录。

## Agent 任务隔离价值

AI coding agent 可能同时接多个任务。如果多个 Agent 共用一个目录，会出现：

- Agent A 切到分支 A，Agent B 的上下文突然变了。
- Agent A 修改文件，Agent B 的测试结果混入了别人的改动。
- 多个任务的 diff 混在一起，难以审计。
- 清理临时文件时不知道哪些属于哪个任务。

Worktree 可以把每个任务放进独立目录：

```text
repo/                -> master
../task-login/       -> task-login
../task-report/      -> task-report
../task-permission/  -> task-permission
```

这样每个 Agent 都能在自己的目录里修改、测试、提交。它们共享仓库历史，但工作区互不干扰。

## 与任务看板的关系

前一节 `.tasks` 看板解决“有哪些任务、谁认领、依赖状态如何”的问题。

本节 worktree 解决“任务被认领后，在哪个隔离工作目录里执行”的问题。

把两者连起来，一个 Agent Harness 可以做到：

1. 从 `.tasks` 读取任务。
2. claim 一个可执行任务。
3. 为该任务创建 worktree 和 branch。
4. 在隔离目录里修改代码。
5. 完成后提交、审计、清理 worktree。

## 判断与行动清单

> [!todo] 使用 worktree 前先检查
> - [ ] 当前目录是否是 Git 仓库。
> - [ ] 新任务是否需要独立工作目录。
> - [ ] 新分支是否应该从 `master` / `main` 创建。
> - [ ] 创建新分支时是否使用 `-b`。
> - [ ] 恢复已有分支时是否去掉 `-b`。
> - [ ] 是否能用 `git worktree list` 查看所有目录。
> - [ ] 任务完成后是否确认 PR / merge 状态再 remove。
> - [ ] 是否理解 remove 不会自动删除分支。

## 应用与迁移问答

> [!question] worktree 和多 clone 仓库有什么区别？
> 多 clone 是复制多份仓库；worktree 是从同一个仓库挂出多个工作目录，管理上更集中，也更适合任务级隔离。

> [!question] 删除 worktree 后为什么还能恢复？
> 因为分支仍然存在。只要分支没删，就能用 `git worktree add <目录> <已有分支>` 重新挂载。

> [!question] worktree 是否等于并行开发？
> 它提供并行开发的目录基础，但真正的并行还需要任务分配、测试、提交、审计和合并策略。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 以为有多个分支就等于有多个工作目录。
> - 把 `git worktree remove` 误解成删除分支。
> - 已有分支恢复时还使用 `-b`。
> - 把 worktree 当成完整 clone 的替代说法。
> - 忘记 worktree 的主要价值是工作区隔离。
> - 多个 Agent 共用一个目录，导致分支和文件状态互相污染。

## 费曼解释润色版

> [!quote]
> Git Worktree 可以让同一个仓库挂出多个工作目录。普通 `git checkout -b` 虽然能创建多个分支，但同一个目录同一时刻只能处在一个分支上，所以多个任务只能轮流做。使用 `git worktree add ../dev-branch-3 -b dev-branch-3 master`，可以创建一个新的目录和分支；再创建 `dev-branch-4`，就能让两个任务在两个目录里同时推进。`git worktree list` 可以查看当前有哪些工作目录。任务完成后，`git worktree remove ../dev-branch-3` 删除的是这个工作目录，不会自动删除分支；如果分支还在，可以用 `git worktree add ../dev-branch-3 dev-branch-3` 恢复。对 AI coding agent 来说，worktree 的价值是把每个任务放进独立目录，避免多个 Agent 共用同一工作区时互相切分支、互相污染文件和测试结果。

## 易错卡片

> [!warning] 误区：多个 branch 就等于多个工作目录
> 正确说法：branch 是提交指针，worktree 才是独立可编辑目录。

> [!warning] 误区：`git worktree remove` 会删除分支
> 正确说法：它主要删除 worktree 目录，分支通常仍然保留。

> [!warning] 误区：恢复已有分支时继续用 `-b`
> 正确说法：`-b` 用于新建分支；已有分支直接指定分支名。

> [!warning] 误区：worktree 只是给人类开发者方便一点
> 正确说法：在 AI coding agent 场景中，它是任务隔离和结果审计的重要基础设施。
