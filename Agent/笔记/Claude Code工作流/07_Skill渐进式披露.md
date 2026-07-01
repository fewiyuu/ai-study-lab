---
title: 07_Skill渐进式披露
aliases:
  - Skill渐进式披露
  - Learn Claude Code 07
tags:
  - LearnClaudeCode
  - Agent
  - Skill
  - context-engineering
  - learning-kit
source: https://www.bilibili.com/video/BV1JfwEzkEbd
created: 2026-06-06
---

> [!question] 常见问题速查
> 1. Skill 文件通常分成哪两部分？
> 2. `SkillLoader` 启动时做了什么？
> 3. 为什么要递归扫描 `skills` 目录？
> 4. 初始 system prompt 为什么只放 `name` 和 `description`？
> 5. `load_skill` 在什么时候被调用？
> 6. 为什么渐进式披露能改善上下文工程？

> [!abstract] 核心主线
> Skill 是给 Agent 的能力说明书，通常写在 `SKILL.md` 里。文件上半部分是 metadata，例如 `name` 和 `description`，用于让模型发现有哪些能力；下半部分是 body，写完整工作流。程序启动时，`SkillLoader` 递归扫描所有 `SKILL.md`，解析 metadata/body，并登记到本地字典。初始 system prompt 只发送 Skill 名称和描述；当模型判断任务需要某个 Skill 时，调用 `load_skill(name)`，本地再把对应 body 作为工具结果写回 messages。这就是渐进式披露。

## 概念精讲

### Skill 是能力说明书

Skill 不是普通聊天记录，也不只是一个工具名。它是一份告诉 Agent 如何完成某类任务的说明书，里面会写触发场景、执行步骤、约束和验收方式。

一个典型 `SKILL.md`：

```markdown
---
name: pdf
description: Create PDF documents from text, Markdown, or generated content.
---

# PDF Skill

1. Clarify the target format and page size.
2. Generate a source document.
3. Render or compile it into a PDF.
4. Verify the output file exists and is readable.
```

判断句：metadata 用于发现能力，body 用于执行能力。

### `SkillLoader` 建立本地索引

程序启动时会创建 `SkillLoader`，扫描 `skills` 目录下所有 `SKILL.md`。真实项目里 Skill 可能在子目录中，所以要递归扫描。

```python
class SkillLoader:
    def __init__(self, skills_dir):
        self.skills_dir = skills_dir
        self.skills = {}
        self.load_all()

    def load_all(self):
        for path in sorted(self.skills_dir.rglob("SKILL.md")):
            text = path.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(text)
            name = metadata["name"]
            self.skills[name] = {
                "metadata": metadata,
                "body": body,
                "path": str(path),
            }
```

这个字典的 key 是 Skill 名称，value 里保存 metadata、body 和路径。路径不是必须给模型看，但对调试、审计和错误提示有用。

## 关键机制

### 初始只发送 Skill 描述

加载器已经把所有 Skill 读到本地，不代表全部内容都要发给模型。`get_descriptions()` 只抽取 `name` 和 `description`，拼成短列表放进 system prompt。

```python
def get_descriptions(self):
    lines = []
    for name, skill in self.skills.items():
        desc = skill["metadata"].get("description", "")
        lines.append(f"- {name}: {desc}")
    return "\n".join(lines)
```

这样模型第一次只知道“有哪些技能、分别适合什么任务”，不会被大量完整工作流淹没。

> [!warning] 易混点
> “本地已经扫描 Skill”不等于“模型已经看到完整 Skill”。本地可以保存所有 body，但初始上下文只放描述。

### 按需调用 `load_skill`

当用户要求创建 PDF，模型看见 PDF Skill 的描述后，会调用 `load_skill`。本地工具根据名称从 `skills` 字典里取出对应 body，并把 body 作为工具结果写回 messages。

```python
def load_skill(name: str) -> str:
    skill = loader.skills.get(name)
    if not skill:
        return f"Skill not found: {name}"
    return skill["body"]
```

下一轮模型请求时，messages 里已经包含完整 Skill 工作流，它就可以继续调用 write、bash 等工具完成任务。

### 渐进式披露的价值

渐进式披露解决的是上下文工程问题。如果有 100 个或 1000 个 Skill，一开始把所有 body 都发给模型，会挤占上下文窗口，让模型在无关说明中找相关信息。

更好的做法：

1. 本地全量扫描，建立索引。
2. 初始只发简短描述。
3. 模型按任务选择 Skill。
4. `load_skill` 返回当前需要的完整 body。
5. body 写回 messages，模型按说明执行。

## 判断与行动清单

> [!todo] 实现 Skill 加载前先检查
> - [ ] 是否递归扫描 `skills` 目录。
> - [ ] 是否只匹配 `SKILL.md`。
> - [ ] 是否能解析 metadata 和 body。
> - [ ] metadata 是否至少包含 `name` 和 `description`。
> - [ ] 本地是否保存 body，但初始 prompt 只发送描述。
> - [ ] `load_skill` 是否能根据 name 找到 body。
> - [ ] `load_skill` 的结果是否写回 messages。
> - [ ] 找不到 Skill 时是否返回清晰错误。

## 应用与迁移问答

> [!question] 为什么 description 不能写得像完整 body？
> description 是给模型做初筛的，应该短而明确。写得太长会让能力目录变成半个说明书，削弱渐进式披露的意义。

> [!question] 找不到 Skill 怎么办？
> 应返回清晰错误，例如 `Skill not found: pdf`，并可列出可用 Skill 名称。更稳的实现还可以做大小写归一化或别名匹配。

> [!question] 渐进式披露和子 Agent 有什么相似点？
> 二者都在控制主上下文的信息密度。子 Agent 隔离子任务中间过程，Skill 则延迟加载完整工作流。

## 练习 / 盲区复盘

> [!failure] 容易卡住的地方
> - 把 metadata 和 body 混在一起。
> - 启动时把所有 Skill body 塞进 system prompt。
> - 只扫描 `skills` 第一层目录，漏掉子目录。
> - `load_skill` 找到 body 后没有写回 messages。
> - Skill 名称大小写不一致导致查找失败。
> - description 写得太空，模型无法判断何时加载。
> - body 写得像宣传文案，没有可执行步骤。

## 费曼解释润色版

> [!quote]
> Skill 是 Agent 的能力说明书，通常写在 `SKILL.md` 中。文件开头的 metadata 记录 `name` 和 `description`，用于让模型知道有哪些能力；下面的 body 才是完整工作流。程序启动时，`SkillLoader` 会递归扫描所有 `SKILL.md`，解析出 metadata 和 body，并存在本地字典里。初始 system prompt 不会发送所有 body，只发送每个 Skill 的名称和描述。模型根据这些描述判断某个任务需要哪个 Skill，再调用 `load_skill(name)`。本地工具把对应 body 作为工具结果写回 messages。这样模型在需要时才看到详细说明，避免一开始用大量无关 Skill 挤占上下文窗口。

## 易错卡片

> [!warning] 误区：加载器读到了 body，模型就自动知道 body
> 正确说法：只有写入 prompt 或 messages 的内容，模型下一轮才看得到。

> [!warning] 误区：Skill 越多，system prompt 就应该越长
> 正确说法：Skill 越多，越需要渐进式披露。

> [!warning] 误区：`load_skill` 只是打印内容
> 正确说法：它要把 Skill body 作为工具结果写回 messages，供下一轮模型使用。

> [!warning] 误区：description 可以很随意
> 正确说法：description 是模型选择 Skill 的依据，必须短、准、可触发。
