from __future__ import annotations

import html
import json
import posixpath
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path, PurePosixPath
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"

PUBLIC_COURSES = [
    {
        "topic": "大语言模型 / LLM 基础与应用工程",
        "root": "大语言模型/研习资料/阶段4-5_LLM基础与应用工程",
        "tags": ["大语言模型", "工程基础"],
    },
    {
        "topic": "大语言模型 / 提示工程",
        "root": "大语言模型/研习资料/提示工程学习笔记",
        "tags": ["大语言模型", "提示工程"],
    },
    {
        "topic": "大语言模型 / RAG 论文精读",
        "root": "大语言模型/研习资料/RAG论文精读",
        "tags": ["大语言模型", "RAG"],
    },
    {
        "topic": "大语言模型 / Harness Engineering",
        "root": "大语言模型/研习资料/Harness Engineering",
        "tags": ["大语言模型", "工程实践"],
    },
    {
        "topic": "大语言模型 / MCP 入门",
        "root": "大语言模型/研习资料/MCP入门",
        "tags": ["大语言模型", "MCP"],
    },
    {
        "topic": "AI 大模型 / 多智能体系统",
        "root": "AI大模型/研习资料/多智能体系统_何时以及如何使用",
        "tags": ["AI大模型", "多智能体"],
    },
    {
        "topic": "Agent",
        "root": "Agent/研习资料",
        "tags": ["Agent"],
    },
    {
        "topic": "Agent Skills",
        "root": "Agent Skills/研习资料",
        "tags": ["Agent", "Skills"],
    },
    {
        "topic": "Context Engineering",
        "root": "Context Engineering/研习资料",
        "tags": ["Agent", "Context Engineering"],
    },
    {
        "topic": "Learn Claude Code",
        "root": "Learn claude code/研习资料",
        "tags": ["Claude Code", "Agent"],
    },
    {
        "topic": "深度学习 / PyTorch 与大模型基础",
        "root": "深度学习/研习资料",
        "tags": ["深度学习", "PyTorch", "大模型基础"],
        "include": "direct",
    },
    {
        "topic": "算法",
        "root": "算法/研习资料/01_数据结构与数组字符串",
        "tags": ["算法", "数据结构与数组字符串"],
    },
    {
        "topic": "算法",
        "root": "算法/研习资料/02_树堆图与结构设计",
        "tags": ["算法", "树堆图与结构设计"],
    },
    {
        "topic": "算法",
        "root": "算法/研习资料/03_回溯动态规划与综合题",
        "tags": ["算法", "回溯动态规划与综合题"],
    },
    {
        "topic": "算法",
        "root": "算法/研习资料",
        "tags": ["算法", "哈希表补充"],
        "include": "direct",
    },
    {
        "topic": "深度学习 / Transformer 论文精读",
        "root": "深度学习/研习资料/Transformer论文精读",
        "tags": ["深度学习", "Transformer"],
    },
    {
        "topic": "PyTorch 深度学习实践",
        "root": "PyTorch深度学习实践 刘二大人/研习资料",
        "tags": ["PyTorch", "深度学习"],
    },
    {
        "topic": "李宏毅 LLM 大模型",
        "root": "李宏毅 LLM大模型/研习资料",
        "tags": ["李宏毅", "大语言模型"],
    },
    {
        "topic": "李宏毅机器学习",
        "root": "李宏毅  机器学习/研习资料",
        "tags": ["李宏毅", "机器学习"],
    },
    {
        "topic": "LoRA 论文精读",
        "root": "LoRA论文精读/研习资料",
        "tags": ["LoRA", "论文精读"],
    },
    {
        "topic": "计算机教育中缺失的一课",
        "root": "计算机教育中缺失的一课/研习资料",
        "tags": ["工程基础"],
    },
]

LESSON_HTML_EXCLUDE = {"index.html", "课程索引.html"}

COURSE_PROFILES = {
    "大语言模型 / LLM 基础与应用工程": {
        "title": "LLM 基础与应用工程",
        "summary": "从 tokenizer、Transformer、RAG、Agent 到成本可靠性，建立大模型应用工程的最小闭环。",
        "audience": "想把大模型概念落到工程实现的人。",
        "firstStep": "先读 tokenizer、embedding、context window。",
        "outcome": "能说清 LLM 应用里模型、检索、提示、评测和约束各自负责什么。",
        "level": "入门到进阶",
        "status": "ready",
    },
    "大语言模型 / 提示工程": {
        "title": "提示工程",
        "summary": "按结构、样本、推理、搜索和知识增强拆开提示词方法。",
        "audience": "想把 prompt 从玄学变成可复用方法的人。",
        "firstStep": "先读提示工程基础与提示词结构。",
        "outcome": "能为任务写出更稳定、可检查、可迭代的提示。",
        "level": "入门",
        "status": "ready",
    },
    "大语言模型 / RAG 论文精读": {
        "title": "RAG 论文精读",
        "summary": "精读 Retrieval-Augmented Generation，把检索、生成、训练和边界连起来。",
        "audience": "想读懂 RAG 原论文，而不只会搭 demo 的人。",
        "firstStep": "先读参数记忆与非参数记忆。",
        "outcome": "能解释 RAG-Sequence、RAG-Token 和检索坍塌等核心问题。",
        "level": "进阶",
        "status": "ready",
    },
    "大语言模型 / Harness Engineering": {
        "title": "Harness Engineering",
        "summary": "把模型能力放进文档、工具、测试、反馈和权限组成的工程环境。",
        "audience": "正在用 Agent 或 Codex 做真实任务的人。",
        "firstStep": "先读角色转变与环境设计。",
        "outcome": "能设计让 AI 稳定工作的仓库环境和反馈回路。",
        "level": "进阶",
        "status": "ready",
    },
    "大语言模型 / MCP 入门": {
        "title": "MCP 入门",
        "summary": "理解 MCP 为什么存在、基本架构是什么，以及什么时候值得采用。",
        "audience": "想判断 MCP 是否适合自己项目的人。",
        "firstStep": "先读 MCP 为什么存在。",
        "outcome": "能区分 MCP、工具调用和普通 API 集成的边界。",
        "level": "入门",
        "status": "ready",
    },
    "AI 大模型 / 多智能体系统": {
        "title": "多智能体系统",
        "summary": "按何时使用、如何拆上下文、如何验证来理解多智能体系统。",
        "audience": "想避免为了 Multi-Agent 而 Multi-Agent 的人。",
        "firstStep": "先读先单智能体与决策框架。",
        "outcome": "能判断什么时候需要多智能体，以及如何切上下文边界。",
        "level": "进阶",
        "status": "ready",
    },
    "Agent": {
        "title": "Agent",
        "summary": "从 ReAct 循环到工程架构、设计模式、评测安全和 Multi-Agent。",
        "audience": "想系统理解 Agent 工程而不是只看概念的人。",
        "firstStep": "先读 ReAct 与 Agent 循环。",
        "outcome": "能把 Agent 描述成可运行、可评测、可约束的系统。",
        "level": "入门到进阶",
        "status": "ready",
    },
    "Agent Skills": {
        "title": "Agent Skills",
        "summary": "学习 Skill 的定位、结构、脚本资源、上下文经济和发布安全。",
        "audience": "想给 Codex/Agent 做可复用能力包的人。",
        "firstStep": "先读技能的定位与渐进披露。",
        "outcome": "能设计一个有触发边界、有资源组织、有验证方式的 Skill。",
        "level": "进阶",
        "status": "ready",
    },
    "Context Engineering": {
        "title": "Context Engineering",
        "summary": "从 Prompt 走向 Context，理解状态、存储、运行时和上下文策略。",
        "audience": "已经写过 prompt，开始被上下文长度和质量折磨的人。",
        "firstStep": "先读从 Prompt 到 Context。",
        "outcome": "能用 Write、Select、Compress、Isolate 四类策略管理上下文。",
        "level": "进阶",
        "status": "ready",
    },
    "Learn Claude Code": {
        "title": "Learn Claude Code",
        "summary": "按 Agent 运行机制拆 Claude Code，从本地启动、工具调用到子 Agent 和任务持久化。",
        "audience": "想理解 Claude Code/Codex 类工具内部工作方式的人。",
        "firstStep": "先读本地启动最小 Agent。",
        "outcome": "能解释一个代码 Agent 如何计划、调用工具、压缩上下文和恢复任务。",
        "level": "入门到进阶",
        "status": "ready",
    },
    "算法": {
        "title": "算法",
        "summary": "按数组链表、哈希、树堆图、回溯动态规划组织常见算法题型。",
        "audience": "想快速建立题型地图和模板意识的人。",
        "firstStep": "先读数组链表与环形数组。",
        "outcome": "能识别常见题型，并知道从哪个框架切入。",
        "level": "入门到面试",
        "status": "ready",
    },
    "深度学习 / PyTorch 与大模型基础": {
        "title": "PyTorch 与大模型基础",
        "summary": "从数据加载、Module、训练循环走到 Tokenizer、Transformer、Eval、RAG 和 Agent 的入门地图。",
        "audience": "想把深度学习训练闭环和大模型应用概念接起来的人。",
        "firstStep": "先读数据加载，再确认 Module、优化器和最小训练循环。",
        "outcome": "能说清训练代码的最小闭环，并知道大模型应用链路里各组件的职责。",
        "level": "入门到实践",
        "status": "drafting",
    },
    "深度学习 / Transformer 论文精读": {
        "title": "Transformer 论文精读",
        "summary": "围绕自注意力、QKV、多头注意力、编码器解码器和位置编码精读 Transformer。",
        "audience": "想真正读懂 Transformer 结构的人。",
        "firstStep": "先读自注意力与 QKV。",
        "outcome": "能把 Transformer 的关键结构用自己的话讲清楚。",
        "level": "进阶",
        "status": "ready",
    },
    "PyTorch 深度学习实践": {
        "title": "PyTorch 深度学习实践",
        "summary": "从线性模型、反向传播、DataLoader 到 CNN/RNN，按代码实践学习深度学习。",
        "audience": "想用 PyTorch 跑通最小训练闭环的人。",
        "firstStep": "先读课程概览与深度学习实践路线。",
        "outcome": "能写出基本训练循环，并理解 Module、Loss、Optimizer 和数据加载。",
        "level": "入门到实践",
        "status": "ready",
    },
    "李宏毅 LLM 大模型": {
        "title": "李宏毅 LLM 大模型",
        "summary": "围绕李宏毅大模型课程制作的长线学习页，适合按专题选读。",
        "audience": "想跟一门完整 LLM 课程慢慢补全背景的人。",
        "firstStep": "从课程导览或最感兴趣的专题开始。",
        "outcome": "能把 LLM 的训练、评估、安全、多模态和生成模型串成课程地图。",
        "level": "长线课程",
        "status": "drafting",
    },
    "李宏毅机器学习": {
        "title": "李宏毅机器学习",
        "summary": "按李宏毅机器学习课程 P 编号整理的完整学习页。",
        "audience": "想系统补机器学习和深度学习基础的人。",
        "firstStep": "先读机器学习基本概念简介。",
        "outcome": "能按课程顺序建立机器学习、深度学习和生成模型基础。",
        "level": "长线课程",
        "status": "drafting",
    },
    "LoRA 论文精读": {
        "title": "LoRA 论文精读",
        "summary": "从 PEFT 动机、低秩更新公式到 Transformer 中的 LoRA 和实验解读。",
        "audience": "想理解大模型高效微调的人。",
        "firstStep": "先读为什么大模型微调需要 PEFT。",
        "outcome": "能解释 LoRA 为什么有效，以及 rank、低秩和实验结论如何读。",
        "level": "进阶",
        "status": "ready",
    },
    "计算机教育中缺失的一课": {
        "title": "计算机教育中缺失的一课",
        "summary": "Shell、文本处理、Git、调试、安全和工程协作的基础工具课。",
        "audience": "想补齐开发者基本功的人。",
        "firstStep": "先读 Shell 基础与路径导航。",
        "outcome": "能更顺地使用命令行、Git、调试工具和自动化脚本。",
        "level": "基础",
        "status": "ready",
    },
}

LEARNING_PATHS = [
    {
        "id": "llm-application",
        "title": "LLM 应用工程线",
        "subtitle": "先搞清模型边界，再进入提示、RAG、协议和工程环境。",
        "audience": "适合想做大模型应用，而不是只收藏概念的人。",
        "outcome": "完成后应能设计一个可评测、可维护的 LLM 应用最小系统。",
        "stages": [
            {
                "topic": "大语言模型 / LLM 基础与应用工程",
                "goal": "建立 LLM 应用的底层地图：模型、上下文、检索、评测和约束。",
            },
            {
                "topic": "大语言模型 / 提示工程",
                "goal": "把 prompt 从随手写变成有结构、有样本、有验收的输入协议。",
            },
            {
                "topic": "大语言模型 / RAG 论文精读",
                "goal": "读懂 RAG 的检索生成分工、概率模型和系统边界。",
            },
            {
                "topic": "大语言模型 / MCP 入门",
                "goal": "判断 MCP 什么时候是协议收益，什么时候只是额外复杂度。",
            },
            {
                "topic": "大语言模型 / Harness Engineering",
                "goal": "把模型能力放进可读、可测、可恢复的工程环境。",
            },
        ],
    },
    {
        "id": "agent-systems",
        "title": "Agent 系统线",
        "subtitle": "从单 Agent 循环走到技能、上下文和多智能体边界。",
        "audience": "适合已经会调用模型，想让 Agent 真正做事的人。",
        "outcome": "完成后应能设计一个有工具、有上下文、有验证边界的 Agent 工作流。",
        "stages": [
            {
                "topic": "Agent",
                "goal": "先把 Agent 看成可运行系统，而不是聊天框里的角色扮演。",
            },
            {
                "topic": "Agent Skills",
                "goal": "学习如何把能力封装成可触发、可复用、可验证的 Skill。",
            },
            {
                "topic": "Context Engineering",
                "goal": "处理 Agent 的状态、记忆、压缩和上下文隔离问题。",
            },
            {
                "topic": "AI 大模型 / 多智能体系统",
                "goal": "判断什么时候需要多智能体，以及如何拆角色和验证边界。",
            },
            {
                "topic": "Learn Claude Code",
                "goal": "用代码 Agent 的运行机制反推真实工程里的规划、工具和恢复能力。",
            },
        ],
    },
    {
        "id": "deep-learning",
        "title": "深度学习到 Transformer 线",
        "subtitle": "从 PyTorch 训练闭环走到 Transformer、LoRA 和长线 LLM 课程选读。",
        "audience": "适合想补模型基础，不想只停在 API 调用层的人。",
        "outcome": "完成后应能读懂基础训练流程、Transformer 结构和高效微调思路。",
        "stages": [
            {
                "topic": "PyTorch 深度学习实践",
                "goal": "跑通深度学习最小训练闭环，理解 Module、Loss、Optimizer 和数据管道。",
            },
            {
                "topic": "深度学习 / PyTorch 与大模型基础",
                "goal": "把训练循环、Transformer、HuggingFace、Eval、RAG 和 Agent 连成应用前置地图。",
            },
            {
                "topic": "深度学习 / Transformer 论文精读",
                "goal": "拆开自注意力、QKV、多头注意力、编码器解码器和位置编码。",
            },
            {
                "topic": "LoRA 论文精读",
                "goal": "理解 PEFT、低秩更新和 LoRA 放进 Transformer 的方式。",
            },
            {
                "topic": "李宏毅 LLM 大模型",
                "goal": "把 LLM 训练、评估、安全、多模态和生成模型当作长线专题选读。",
            },
        ],
    },
    {
        "id": "engineering-foundation",
        "title": "工程基础线",
        "subtitle": "先补工具链和命令行，再补算法题型地图。",
        "audience": "适合想提升工程基本功、面试题型识别和日常开发效率的人。",
        "outcome": "完成后应能更稳定地使用命令行、Git、调试工具，并识别常见算法框架。",
        "stages": [
            {
                "topic": "计算机教育中缺失的一课",
                "goal": "补 Shell、文本处理、Git、调试、安全和自动化这些长期复利工具。",
            },
            {
                "topic": "算法",
                "goal": "按数组链表、树堆图、回溯动态规划建立题型和模板地图。",
            },
            {
                "topic": "李宏毅机器学习",
                "goal": "作为长线补课入口，系统回看机器学习和深度学习基础。",
            },
        ],
    },
]

STATIC_COURSES = [
    {
        "id": "context-engineering",
        "topic": "Context Engineering",
        "title": COURSE_PROFILES["Context Engineering"]["title"],
        "summary": COURSE_PROFILES["Context Engineering"]["summary"],
        "audience": COURSE_PROFILES["Context Engineering"]["audience"],
        "firstStep": COURSE_PROFILES["Context Engineering"]["firstStep"],
        "outcome": COURSE_PROFILES["Context Engineering"]["outcome"],
        "level": COURSE_PROFILES["Context Engineering"]["level"],
        "status": COURSE_PROFILES["Context Engineering"]["status"],
        "pageCount": 4,
        "entryPath": "Context Engineering/研习资料/01_从 Prompt 到 Context：为什么 Agent 需要上下文工程.html",
        "tags": ["Agent", "Context Engineering"],
        "pages": [
            {
                "topic": "Context Engineering",
                "title": "01 从 Prompt 到 Context：为什么 Agent 需要上下文工程",
                "path": "Context Engineering/研习资料/01_从 Prompt 到 Context：为什么 Agent 需要上下文工程.html",
                "tags": ["Agent", "Context Engineering"],
            },
            {
                "topic": "Context Engineering",
                "title": "02 上下文控制面：State、Store、Runtime 与 Middleware",
                "path": "Context Engineering/研习资料/02_上下文控制面：State、Store、Runtime 与 Middleware.html",
                "tags": ["Agent", "Context Engineering"],
            },
            {
                "topic": "Context Engineering",
                "title": "03 四类策略：Write、Select、Compress、Isolate",
                "path": "Context Engineering/研习资料/03_四类策略：Write、Select、Compress、Isolate.html",
                "tags": ["Agent", "Context Engineering"],
            },
            {
                "topic": "Context Engineering",
                "title": "04 产品案例与工程验收：Claude Code、Manus、Kiro",
                "path": "Context Engineering/研习资料/04_产品案例与工程验收：Claude Code、Manus、Kiro.html",
                "tags": ["Agent", "Context Engineering"],
            },
        ],
    }
]


def to_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def href_from(index_path: str, target_path: str) -> str:
    base_dir = posixpath.dirname(index_path)
    rel = posixpath.relpath(target_path, base_dir)
    return quote(rel, safe="/._-:%#")


def common_course_root(paths: list[str]) -> str:
    parents = [str(PurePosixPath(path).parent) for path in paths]
    if not parents:
        return ""
    return posixpath.commonpath(parents)


def clean_title(path: Path) -> str:
    stem = path.parent.name if path.name == "学习页.html" else path.stem
    stem = re.sub(r"^(P\d+)[_-]?", r"\1 ", stem)
    stem = re.sub(r"^(\d+)[_-]?", r"\1 ", stem)
    return stem.replace("_", " ").strip()


def public_course_title(course: dict[str, object], duplicate_topics: set[str]) -> str:
    topic = str(course["topic"])
    profile = COURSE_PROFILES.get(topic, {})
    title = str(profile.get("title", topic))
    if topic not in duplicate_topics:
        return title
    tags = [str(tag) for tag in course.get("tags", [])]
    if len(tags) > 1:
        return f"{title}：{tags[-1]}"
    root_name = PurePosixPath(str(course["root"])).name
    return f"{title}：{root_name}"


def public_course_summary(course: dict[str, object], duplicate_topics: set[str]) -> str:
    topic = str(course["topic"])
    profile = COURSE_PROFILES.get(topic, {})
    summary = str(profile.get("summary", ""))
    if topic not in duplicate_topics:
        return summary
    tags = [str(tag) for tag in course.get("tags", [])]
    if len(tags) > 1:
        return f"{summary} 本入口聚焦：{tags[-1]}。"
    return summary


def lesson_pages_under(root: Path, include: str = "recursive") -> list[Path]:
    pages: list[Path] = []
    if include == "direct":
        pages.extend(root.glob("*/学习页.html"))
    else:
        pages.extend(root.rglob("学习页.html"))
    pages.extend(
        page
        for page in root.glob("*.html")
        if page.name not in LESSON_HTML_EXCLUDE
    )
    return sorted(set(pages), key=lambda item: item.as_posix())


def lesson_pages_for_course(course: dict[str, object]) -> list[Path]:
    root = ROOT / str(course["root"])
    return lesson_pages_under(root, include=str(course.get("include", "recursive")))


def build_pages() -> list[dict[str, object]]:
    pages: list[dict[str, object]] = []
    seen: set[str] = set()

    for course in PUBLIC_COURSES:
        root = ROOT / course["root"]
        if not root.exists():
            print(f"skip missing: {course['root']}")
            continue

        for page in lesson_pages_for_course(course):
            rel_path = to_posix(page)
            if rel_path in seen:
                continue
            seen.add(rel_path)
            pages.append(
                {
                    "topic": course["topic"],
                    "title": clean_title(page),
                    "path": rel_path,
                    "tags": course["tags"],
                }
            )

    return pages


def build_courses(pages: list[dict[str, object]]) -> list[dict[str, object]]:
    courses: list[dict[str, object]] = []
    topic_order: list[str] = []
    pages_by_topic: dict[str, list[dict[str, object]]] = {}

    for page in pages:
        topic = str(page["topic"])
        if topic not in pages_by_topic:
            pages_by_topic[topic] = []
            topic_order.append(topic)
        pages_by_topic[topic].append(page)

    for topic in topic_order:
        course_pages = pages_by_topic[topic]
        first_page = course_pages[0]
        course_root = common_course_root([str(page["path"]) for page in course_pages])
        index_path = f"{course_root}/index.html" if course_root else str(first_page["path"])
        profile = COURSE_PROFILES.get(topic, {})
        courses.append(
            {
                "id": slugify(topic),
                "topic": topic,
                "title": profile.get("title", topic),
                "summary": profile.get("summary", ""),
                "audience": profile.get("audience", ""),
                "firstStep": profile.get("firstStep", f"先读 {first_page['title']}。"),
                "outcome": profile.get("outcome", ""),
                "level": profile.get("level", ""),
                "status": profile.get("status", "ready"),
                "pageCount": len(course_pages),
                "courseRoot": course_root,
                "indexPath": index_path,
                "entryPath": index_path,
                "firstPagePath": first_page["path"],
                "tags": first_page["tags"],
            }
        )

    static_topics = {str(course["topic"]) for course in courses}
    for static_course in STATIC_COURSES:
        if static_course["topic"] not in static_topics:
            course = {key: value for key, value in static_course.items() if key != "pages"}
            courses.append(course)

    return courses


def build_public_course_indexes(pages: list[dict[str, object]]) -> list[dict[str, object]]:
    pages_by_path = {str(page["path"]): page for page in pages}
    topic_counts: dict[str, int] = {}
    for course in PUBLIC_COURSES:
        topic_counts[str(course["topic"])] = topic_counts.get(str(course["topic"]), 0) + 1
    duplicate_topics = {topic for topic, count in topic_counts.items() if count > 1}

    indexes: list[dict[str, object]] = []
    for course in PUBLIC_COURSES:
        root_path = ROOT / str(course["root"])
        if not root_path.exists():
            continue

        course_pages = [
            pages_by_path[to_posix(page)]
            for page in lesson_pages_for_course(course)
            if to_posix(page) in pages_by_path
        ]
        if not course_pages:
            continue

        topic = str(course["topic"])
        profile = COURSE_PROFILES.get(topic, {})
        root = str(course["root"])
        index_path = f"{root}/index.html"
        indexes.append(
            {
                "id": slugify(f"{topic}-{root}"),
                "topic": topic,
                "title": public_course_title(course, duplicate_topics),
                "summary": public_course_summary(course, duplicate_topics),
                "audience": profile.get("audience", ""),
                "firstStep": profile.get("firstStep", f"先读 {course_pages[0]['title']}。"),
                "outcome": profile.get("outcome", ""),
                "level": profile.get("level", ""),
                "status": profile.get("status", "ready"),
                "pageCount": len(course_pages),
                "courseRoot": root,
                "indexPath": index_path,
                "entryPath": index_path,
                "firstPagePath": course_pages[0]["path"],
                "tags": course.get("tags", []),
                "pages": course_pages,
            }
        )
    return indexes


def course_lookup(courses: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {str(course["topic"]): course for course in courses}


def build_learning_paths(
    pages: list[dict[str, object]],
    courses: list[dict[str, object]],
) -> list[dict[str, object]]:
    pages_by_topic: dict[str, list[dict[str, object]]] = {}
    for page in pages:
        pages_by_topic.setdefault(str(page["topic"]), []).append(page)
    for static_course in STATIC_COURSES:
        pages_by_topic.setdefault(str(static_course["topic"]), static_course["pages"])
    courses_by_topic = course_lookup(courses)

    paths: list[dict[str, object]] = []
    for path in LEARNING_PATHS:
        stages: list[dict[str, object]] = []
        for index, stage in enumerate(path["stages"], start=1):
            topic = stage["topic"]
            stage_pages = pages_by_topic.get(topic, [])
            if not stage_pages:
                print(f"skip missing stage: {topic}")
                continue
            first_page = stage_pages[0]
            course = courses_by_topic.get(topic, {})
            profile = COURSE_PROFILES.get(topic, {})
            stages.append(
                {
                    "order": index,
                    "topic": topic,
                    "title": course.get("title", profile.get("title", topic)),
                    "goal": stage["goal"],
                    "pageCount": len(stage_pages),
                    "entryPath": course.get("entryPath", first_page["path"]),
                    "entryTitle": first_page["title"],
                    "pages": stage_pages,
                }
            )

        paths.append(
            {
                "id": path["id"],
                "title": path["title"],
                "subtitle": path["subtitle"],
                "audience": path["audience"],
                "outcome": path["outcome"],
                "stageCount": len(stages),
                "pageCount": sum(int(stage["pageCount"]) for stage in stages),
                "stages": stages,
            }
        )

    return paths


def course_pages_lookup(pages: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    pages_by_topic: dict[str, list[dict[str, object]]] = {}
    for page in pages:
        pages_by_topic.setdefault(str(page["topic"]), []).append(page)
    for static_course in STATIC_COURSES:
        pages_by_topic.setdefault(str(static_course["topic"]), static_course["pages"])
    return pages_by_topic


def status_label(status: object) -> str:
    labels = {
        "ready": "可学习",
        "drafting": "持续补全",
        "draft": "草稿",
    }
    return labels.get(str(status), str(status) if status else "可学习")


def render_course_index(course: dict[str, object], pages: list[dict[str, object]]) -> str:
    index_path = str(course.get("indexPath") or course.get("entryPath") or "")
    title = str(course.get("title") or course.get("topic") or "课程入口")
    topic = str(course.get("topic") or title)
    summary = str(course.get("summary") or "这是一组可按顺序学习的公开学习页。")
    audience = str(course.get("audience") or "适合想按路径系统学习的读者。")
    outcome = str(course.get("outcome") or "完成后应能把核心概念、例子和常见误区串起来。")
    first_step = str(course.get("firstStep") or (f"先读 {pages[0]['title']}。" if pages else "从第一节开始。"))
    level = str(course.get("level") or "学习路径")
    tags = [str(tag) for tag in course.get("tags", [])]
    home_href = href_from(index_path, "index.html") if index_path else "../../index.html"
    first_href = href_from(index_path, str(pages[0]["path"])) if pages else "#"

    page_cards = []
    for index, page in enumerate(pages, start=1):
        page_href = href_from(index_path, str(page["path"]))
        page_title = html.escape(str(page["title"]))
        page_cards.append(
            f"""
          <article class="unit" id="unit-{index:02d}">
            <div class="unit-number">{index:02d}</div>
            <div>
              <h3>{page_title}</h3>
              <p>{html.escape(topic)}</p>
            </div>
            <a href="{page_href}">打开学习页</a>
          </article>"""
        )

    path_nodes = "\n".join(
        f'<a href="#unit-{index:02d}"><span>{index:02d}</span>{html.escape(str(page["title"]))}</a>'
        for index, page in enumerate(pages, start=1)
    )
    tags_html = "\n".join(f'<span class="chip">{html.escape(tag)}</span>' for tag in tags)
    cards_html = "\n".join(page_cards)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}｜课程地图</title>
  <meta name="description" content="{html.escape(summary)}">
  <style>
    :root {{
      --paper:#f6f2e8;--paper-2:#eee7d9;--ink:#171717;--muted:#655f52;--line:#d6cdbb;
      --panel:#fffdf7;--panel-2:#f9f5eb;--accent:#1d5f8f;--green:#2d6a55;--red:#ad3e33;
      --shadow:0 18px 45px rgba(34,30,22,.08);
      --mono:"Cascadia Code","SFMono-Regular",Consolas,monospace;
      --sans:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;
      --serif:"Songti SC","Noto Serif CJK SC",SimSun,serif;
    }}
    *{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
    body{{margin:0;min-height:100vh;color:var(--ink);font-family:var(--sans);line-height:1.66;background:
      linear-gradient(90deg,rgba(23,23,23,.045) 1px,transparent 1px) 0 0/42px 42px,
      linear-gradient(rgba(23,23,23,.035) 1px,transparent 1px) 0 0/42px 42px,var(--paper)}}
    a{{color:inherit}}.layout{{display:grid;grid-template-columns:320px minmax(0,1fr);min-height:100vh}}
    aside{{position:sticky;top:0;height:100vh;overflow:auto;padding:28px 22px;border-right:1px solid var(--line);background:rgba(255,253,247,.9);backdrop-filter:blur(14px)}}
    .mark{{display:inline-grid;place-items:center;width:42px;height:42px;margin-bottom:16px;background:var(--ink);color:#fff;font-family:var(--mono);font-weight:800}}
    h1{{margin:0;font-family:var(--serif);font-size:42px;line-height:1.04;letter-spacing:0}}.subtitle{{margin:14px 0 0;color:var(--muted);font-size:14px}}
    .side-label{{display:block;margin:22px 0 7px;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}}
    .path-nav{{display:grid;gap:7px}}.path-nav a{{display:grid;grid-template-columns:42px minmax(0,1fr);gap:8px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line);color:var(--muted);text-decoration:none;font-size:13px}}
    .path-nav a:hover{{color:var(--ink)}}.path-nav span{{font-family:var(--mono);color:var(--red);font-weight:800}}
    main{{min-width:0;padding:42px clamp(18px,4vw,64px) 64px}}.hero{{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,420px);gap:28px;align-items:end;padding-bottom:28px;border-bottom:1px solid var(--line)}}
    .kicker{{width:max-content;max-width:100%;padding:4px 8px;border:1px solid var(--ink);background:var(--panel);font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase}}
    .hero h2{{margin:18px 0 0;max-width:13ch;font-family:var(--serif);font-size:clamp(40px,6vw,76px);line-height:.98;letter-spacing:0}}
    .hero-copy{{color:var(--muted);font-size:16px}}.hero-copy a{{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(29,95,143,.35)}}
    .chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}}.chip{{display:inline-flex;align-items:center;min-height:26px;padding:3px 8px;border:1px solid var(--line);background:var(--panel);color:var(--muted);font-size:12px}}.chip.strong{{border-color:var(--ink);color:var(--ink);font-family:var(--mono)}}
    .panel{{margin-top:26px;border:1px solid var(--line);background:rgba(255,253,247,.72);box-shadow:var(--shadow)}}.panel-head{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;padding:22px 24px;border-bottom:1px solid var(--line);background:var(--panel)}}
    .panel-head h2{{margin:0;font-family:var(--serif);font-size:clamp(26px,4vw,40px);line-height:1.12}}.panel-head p{{margin:8px 0 0;color:var(--muted)}}.count{{padding:4px 8px;border:1px solid var(--line);background:var(--paper-2);color:var(--muted);font-family:var(--mono);font-size:12px;white-space:nowrap}}
    .meta-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line)}}.meta{{padding:18px;background:var(--panel)}}.meta b{{display:block;margin-bottom:8px;font-family:var(--mono);font-size:12px;color:var(--green);letter-spacing:.08em}}.meta p{{margin:0;color:var(--muted)}}
    .units{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1px;background:var(--line)}}.unit{{display:grid;grid-template-rows:auto 1fr auto;min-height:220px;padding:18px;background:var(--panel)}}
    .unit-number{{font-family:var(--mono);font-size:13px;color:var(--red);font-weight:800}}.unit h3{{margin:12px 0 0;font-size:20px;line-height:1.28}}.unit p{{margin:10px 0 0;color:var(--muted);font-size:13px}}.unit a,.primary{{display:inline-flex;align-items:center;justify-content:center;min-height:36px;margin-top:16px;padding:7px 10px;border:1px solid var(--ink);background:var(--ink);color:#fff;text-decoration:none;font-size:13px;font-weight:700}}.unit a:hover,.primary:hover{{background:var(--accent);border-color:var(--accent)}}
    @media(max-width:900px){{.layout{{grid-template-columns:1fr}}aside{{position:static;height:auto}}.hero,.meta-grid{{grid-template-columns:1fr}}main{{padding:24px 16px 44px}}.hero h2{{font-size:38px}}}}
  </style>
</head>
<body>
  <div class="layout">
    <aside>
      <div class="mark">MAP</div>
      <h1>{html.escape(title)}</h1>
      <p class="subtitle">{html.escape(summary)}</p>
      <span class="side-label">小节</span>
      <nav class="path-nav">
        {path_nodes}
      </nav>
    </aside>
    <main>
      <section class="hero">
        <div>
          <div class="kicker">课程地图</div>
          <h2>{html.escape(title)}</h2>
          <div class="chips">
            <span class="chip strong">{html.escape(str(len(pages)))} 节课</span>
            <span class="chip">{html.escape(level)}</span>
            <span class="chip">{html.escape(status_label(course.get("status")))}</span>
            {tags_html}
          </div>
        </div>
        <div class="hero-copy">
          <p>{html.escape(summary)}</p>
          <p><b>第一步：</b>{html.escape(first_step)}</p>
          <a class="primary" href="{first_href}">开始第一节</a>
          <p><a href="{home_href}">返回 AI Study Lab</a></p>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <h2>学习路径</h2>
            <p>先按顺序走一遍，再按需要回看具体小节。</p>
          </div>
          <span class="count">{html.escape(str(len(pages)))} 小节</span>
        </div>
        <div class="meta-grid">
          <div class="meta"><b>适合对象</b><p>{html.escape(audience)}</p></div>
          <div class="meta"><b>学完能做</b><p>{html.escape(outcome)}</p></div>
          <div class="meta"><b>主题</b><p>{html.escape(topic)}</p></div>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <h2>全部小节</h2>
            <p>每个入口都会打开对应的学习页。</p>
          </div>
          <span class="count">点击进入</span>
        </div>
        <div class="units">
          {cards_html}
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def write_course_indexes(
    courses: list[dict[str, object]],
    pages: list[dict[str, object]],
) -> set[str]:
    pages_by_topic = course_pages_lookup(pages)
    written: set[str] = set()
    for course in courses:
        index_path = str(course.get("indexPath") or course.get("entryPath") or "")
        if not index_path or not index_path.endswith("index.html"):
            continue
        course_pages = pages_by_topic.get(str(course["topic"]), [])
        if not course_pages:
            continue
        output_path = ROOT / index_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_course_index(course, course_pages), encoding="utf-8")
        written.add(index_path)
        print(f"wrote {to_posix(output_path)}")
    return written


def write_public_course_indexes(
    indexes: list[dict[str, object]],
    skip_paths: set[str] | None = None,
) -> set[str]:
    written: set[str] = set()
    skip_paths = skip_paths or set()
    for course in indexes:
        index_path = str(course["indexPath"])
        if index_path in skip_paths:
            continue
        course_pages = list(course["pages"])
        output_path = ROOT / index_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_course_index(course, course_pages), encoding="utf-8")
        written.add(index_path)
        print(f"wrote {to_posix(output_path)}")
    return written


def slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "-", slug)
    return slug.strip("-")


def main() -> None:
    tz = timezone(timedelta(hours=8))
    pages = build_pages()
    courses = build_courses(pages)
    learning_paths = build_learning_paths(pages, courses)
    written_indexes = write_course_indexes(courses, pages)
    write_public_course_indexes(build_public_course_indexes(pages), skip_paths=written_indexes)
    data = {
        "generatedAt": datetime.now(tz).isoformat(timespec="seconds"),
        "pageCount": len(pages),
        "courseCount": len(courses),
        "pathCount": len(learning_paths),
        "courses": courses,
        "learningPaths": learning_paths,
        "pages": pages,
    }
    CATALOG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {CATALOG_PATH.name}: {len(pages)} pages")


if __name__ == "__main__":
    main()
