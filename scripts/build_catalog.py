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
        "root": "大语言模型/研习资料/LLM基础与应用工程",
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
        "topic": "Agent / 多智能体系统",
        "root": "Agent/研习资料/多智能体系统",
        "tags": ["Agent", "多智能体"],
    },
    {
        "topic": "Agent / Agent 基础与工程",
        "root": "Agent/研习资料/Agent基础与工程",
        "tags": ["Agent", "基础工程"],
    },
    {
        "topic": "Agent / Agent Skills",
        "root": "Agent/研习资料/Agent Skills",
        "tags": ["Agent", "Skills"],
    },
    {
        "topic": "Agent / Claude Code 工作流",
        "root": "Agent/研习资料/Claude Code工作流",
        "tags": ["Claude Code", "Agent"],
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
        "topic": "大语言模型 / 李宏毅 LLM 课程",
        "root": "大语言模型/研习资料/李宏毅LLM课程",
        "tags": ["李宏毅", "大语言模型"],
    },
    {
        "topic": "李宏毅机器学习",
        "root": "李宏毅  机器学习/研习资料",
        "tags": ["李宏毅", "机器学习"],
    },
    {
        "topic": "LoRA 论文精读",
        "root": "大语言模型/研习资料/LoRA论文精读",
        "tags": ["LoRA", "论文精读"],
    },
    {
        "topic": "计算机教育中缺失的一课",
        "root": "计算机教育中缺失的一课/研习资料",
        "tags": ["工程基础"],
    },
    {
        "topic": "大语言模型 / 从零训练小语言模型",
        "root": "大语言模型/研习资料/从零训练小语言模型",
        "tags": ["大语言模型", "模型训练"],
    },
    {
        "topic": "大语言模型 / 预训练数据工程与数据配方",
        "root": "大语言模型/研习资料/预训练数据工程与数据配方",
        "tags": ["大语言模型", "数据工程"],
    },
    {
        "topic": "大语言模型 / 后训练全栈",
        "root": "大语言模型/研习资料/后训练全栈",
        "tags": ["大语言模型", "后训练"],
    },
    {
        "topic": "大语言模型 / 推理模型训练",
        "root": "大语言模型/研习资料/推理模型训练",
        "tags": ["大语言模型", "推理训练"],
    },
    {
        "topic": "大语言模型 / Agentic 后训练与工具使用 RL",
        "root": "大语言模型/研习资料/Agentic后训练与工具使用RL",
        "tags": ["大语言模型", "Agentic RL"],
    },
    {
        "topic": "AI 基础设施 / GPU 性能工程",
        "root": "AI基础设施/研习资料/GPU性能工程",
        "tags": ["AI 基础设施", "GPU"],
    },
    {
        "topic": "AI 基础设施 / 现代 LLM 推理引擎内核",
        "root": "AI基础设施/研习资料/现代LLM推理引擎内核",
        "tags": ["AI 基础设施", "推理引擎"],
    },
    {
        "topic": "AI 基础设施 / 分布式训练系统",
        "root": "AI基础设施/研习资料/分布式训练系统",
        "tags": ["AI 基础设施", "分布式训练"],
    },
    {
        "topic": "AI 基础设施 / LLM Serving 架构与请求调度",
        "root": "AI基础设施/研习资料/LLMServing架构与请求调度",
        "tags": ["AI 基础设施", "Serving"],
    },
    {
        "topic": "Agent / Agent Harness Engineering",
        "root": "Agent/研习资料/AgentHarnessEngineering",
        "tags": ["Agent", "Harness"],
    },
    {
        "topic": "Agent / 工具调用契约与结构化交互",
        "root": "Agent/研习资料/工具调用契约与结构化交互",
        "tags": ["Agent", "工具调用"],
    },
    {
        "topic": "Agent / Agent 可靠性工程",
        "root": "Agent/研习资料/Agent可靠性工程",
        "tags": ["Agent", "可靠性"],
    },
]

LESSON_HTML_EXCLUDE = {"index.html", "课程索引.html"}

PRESERVE_COURSE_INDEX_ROOTS = {
    "大语言模型/研习资料/从零训练小语言模型",
    "大语言模型/研习资料/预训练数据工程与数据配方",
    "大语言模型/研习资料/后训练全栈",
    "大语言模型/研习资料/推理模型训练",
    "大语言模型/研习资料/Agentic后训练与工具使用RL",
    "AI基础设施/研习资料/GPU性能工程",
    "AI基础设施/研习资料/现代LLM推理引擎内核",
    "AI基础设施/研习资料/分布式训练系统",
    "AI基础设施/研习资料/LLMServing架构与请求调度",
    "Agent/研习资料/AgentHarnessEngineering",
    "Agent/研习资料/工具调用契约与结构化交互",
    "Agent/研习资料/Agent可靠性工程",
}

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
    "Agent / 多智能体系统": {
        "title": "多智能体系统",
        "summary": "按何时使用、如何拆上下文、如何验证来理解多智能体系统。",
        "audience": "想避免为了 Multi-Agent 而 Multi-Agent 的人。",
        "firstStep": "先读先单智能体与决策框架。",
        "outcome": "能判断什么时候需要多智能体，以及如何切上下文边界。",
        "level": "进阶",
        "status": "ready",
    },
    "Agent / Agent 基础与工程": {
        "title": "Agent 基础与工程",
        "summary": "从 ReAct 循环到工程架构、设计模式、评测安全和 Multi-Agent。",
        "audience": "想系统理解 Agent 工程而不是只看概念的人。",
        "firstStep": "先读 ReAct 与 Agent 循环。",
        "outcome": "能把 Agent 描述成可运行、可评测、可约束的系统。",
        "level": "入门到进阶",
        "status": "ready",
    },
    "Agent / Agent Skills": {
        "title": "Agent Skills",
        "summary": "学习 Skill 的定位、结构、脚本资源、上下文经济和发布安全。",
        "audience": "想给 Codex/Agent 做可复用能力包的人。",
        "firstStep": "先读技能的定位与渐进披露。",
        "outcome": "能设计一个有触发边界、有资源组织、有验证方式的 Skill。",
        "level": "进阶",
        "status": "ready",
    },
    "Agent / Context Engineering": {
        "title": "Context Engineering",
        "summary": "从 Prompt 走向 Context，理解状态、存储、运行时和上下文策略。",
        "audience": "已经写过 prompt，开始被上下文长度和质量折磨的人。",
        "firstStep": "先读从 Prompt 到 Context。",
        "outcome": "能用 Write、Select、Compress、Isolate 四类策略管理上下文。",
        "level": "进阶",
        "status": "ready",
    },
    "Agent / Claude Code 工作流": {
        "title": "Claude Code 工作流",
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
    "大语言模型 / 李宏毅 LLM 课程": {
        "title": "李宏毅 LLM 课程",
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
    "大语言模型 / 从零训练小语言模型": {
        "title": "从零训练小语言模型",
        "summary": "从 tokenizer、数据、Transformer、优化器、训练循环到评测，跑通一个小语言模型的完整闭环。",
        "audience": "已经有 PyTorch 和 Transformer 基础，想理解模型能力如何被训练出来的人。",
        "firstStep": "先读课程地图，确认 CS336、llm.c 和 OLMo 2 分别支撑哪些单元。",
        "outcome": "能解释一个小语言模型从数据到训练再到评测的主要环节，并能判断复现实验缺什么。",
        "level": "进阶",
        "status": "planned",
    },
    "大语言模型 / 预训练数据工程与数据配方": {
        "title": "预训练数据工程与数据配方",
        "summary": "学习清洗、去重、过滤、质量评分和混合比例如何影响预训练模型质量。",
        "audience": "想把大模型质量问题追到数据层，而不是只调模型结构的人。",
        "firstStep": "先读数据来源、过滤目标和质量信号的总图。",
        "outcome": "能为小规模预训练或后训练项目设计一条可解释的数据处理管线。",
        "level": "进阶",
        "status": "planned",
    },
    "大语言模型 / 后训练全栈": {
        "title": "后训练全栈",
        "summary": "把 SFT、偏好数据、奖励模型、DPO、PPO/RLHF 和评测串成后训练闭环。",
        "audience": "已经知道 LoRA 或微调概念，想理解模型行为如何被塑形的人。",
        "firstStep": "先区分 SFT、偏好优化和强化学习各自改变什么。",
        "outcome": "能判断一个后训练任务需要哪类数据、哪种优化目标和怎样的验收方式。",
        "level": "进阶",
        "status": "planned",
    },
    "大语言模型 / 推理模型训练": {
        "title": "推理模型训练",
        "summary": "围绕 RLVR、GRPO、蒸馏和可验证奖励，理解推理型模型如何获得长链路解题能力。",
        "audience": "想理解 DeepSeek-R1、Open-R1 和 verl 这类训练路线的人。",
        "firstStep": "先读可验证奖励和普通偏好优化的区别。",
        "outcome": "能说明推理模型训练为什么依赖任务环境、奖励设计、采样和蒸馏。",
        "level": "高级",
        "status": "planned",
    },
    "大语言模型 / Agentic 后训练与工具使用 RL": {
        "title": "Agentic 后训练与工具使用 RL",
        "summary": "研究模型如何通过环境交互、工具轨迹和强化学习学会搜索、调用工具和完成长程任务。",
        "audience": "想把 Agent 系统和模型训练连接起来的人。",
        "firstStep": "先读工具使用轨迹、环境反馈和 credit assignment 的关系。",
        "outcome": "能设计一个小型工具使用训练任务，并知道哪些部分只是系统提示、哪些需要训练信号。",
        "level": "高级",
        "status": "planned",
    },
    "AI 基础设施 / GPU 性能工程": {
        "title": "GPU 性能工程",
        "summary": "从 CUDA、Triton、profiling 和 FlashAttention 入手，理解深度学习计算为什么慢、慢在哪里、怎么优化。",
        "audience": "会写 PyTorch，但想看懂 kernel、显存带宽和 profiling 结果的人。",
        "firstStep": "先建立 GPU 执行模型和 profiling 词表。",
        "outcome": "能读懂一次算子性能分析，并知道何时该用 PyTorch、Triton 或现成高性能 kernel。",
        "level": "高级",
        "status": "planned",
    },
    "AI 基础设施 / 现代 LLM 推理引擎内核": {
        "title": "现代 LLM 推理引擎内核",
        "summary": "学习 PagedAttention、KV cache、连续批处理和调度如何把请求变成高吞吐 token 流。",
        "audience": "想理解 vLLM、SGLang 这类推理系统内部机制的人。",
        "firstStep": "先读 prefill、decode、KV cache 和 batching 的关系。",
        "outcome": "能解释推理引擎的吞吐、延迟、显存和并发之间的主要权衡。",
        "level": "高级",
        "status": "planned",
    },
    "AI 基础设施 / 分布式训练系统": {
        "title": "分布式训练系统",
        "summary": "按 DDP、FSDP、ZeRO、张量并行和 Megatron 拆解大模型训练为什么能扩到多卡多机。",
        "audience": "想理解大模型训练系统，而不是只会启动训练脚本的人。",
        "firstStep": "先弄清参数、梯度、优化器状态和激活分别占什么资源。",
        "outcome": "能判断一个训练任务为什么爆显存、通信慢或 checkpoint 难恢复。",
        "level": "高级",
        "status": "planned",
    },
    "AI 基础设施 / LLM Serving 架构与请求调度": {
        "title": "LLM Serving 架构与请求调度",
        "summary": "把模型服务、网关、路由、批处理、限流、缓存和监控放进一条可上线的 serving 链路。",
        "audience": "想把本地模型或推理服务接进真实产品的人。",
        "firstStep": "先区分推理引擎、模型服务、API 网关和业务系统的边界。",
        "outcome": "能画出一个 LLM serving 架构，并说明吞吐、延迟、成本和稳定性如何验收。",
        "level": "进阶到高级",
        "status": "planned",
    },
    "Agent / Agent Harness Engineering": {
        "title": "Agent Harness Engineering",
        "summary": "把 Agent Loop 放进可运行外壳：工具调度、状态、沙箱、权限、重试、恢复和日志。",
        "audience": "已经理解 Agent 基础，想自己搭可靠执行环境的人。",
        "firstStep": "先读 Agent 运行外壳和普通工具调用的区别。",
        "outcome": "能设计一个可观察、可恢复、可约束的 Agent 执行框架。",
        "level": "进阶",
        "status": "planned",
    },
    "Agent / 工具调用契约与结构化交互": {
        "title": "工具调用契约与结构化交互",
        "summary": "把 JSON Schema、结构化输出、工具协议、错误恢复和跨模型兼容当成 Agent 的接口契约来学习。",
        "audience": "想把工具调用从临场提示变成稳定接口的人。",
        "firstStep": "先读结构化输出和工具 schema 为什么是执行边界。",
        "outcome": "能为一个 Agent 工具集设计清晰 schema、错误策略和结果协议。",
        "level": "进阶",
        "status": "planned",
    },
    "Agent / Agent 可靠性工程": {
        "title": "Agent 可靠性工程",
        "summary": "学习可恢复执行、任务状态、评测、Tracing 和 OpenTelemetry 如何让 Agent 长程任务可诊断。",
        "audience": "已经在做 Agent 或工作流，开始遇到失败不可复现、结果不可验收的人。",
        "firstStep": "先读 durable execution、trace/span 和任务回归测试的关系。",
        "outcome": "能为一个 Agent 项目建立恢复、评测和执行溯源的最小可靠性框架。",
        "level": "高级",
        "status": "planned",
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
                "topic": "Agent / Agent 基础与工程",
                "goal": "先把 Agent 看成可运行系统，而不是聊天框里的角色扮演。",
            },
            {
                "topic": "Agent / Agent Skills",
                "goal": "学习如何把能力封装成可触发、可复用、可验证的 Skill。",
            },
            {
                "topic": "Agent / Context Engineering",
                "goal": "处理 Agent 的状态、记忆、压缩和上下文隔离问题。",
            },
            {
                "topic": "Agent / 多智能体系统",
                "goal": "判断什么时候需要多智能体，以及如何拆角色和验证边界。",
            },
            {
                "topic": "Agent / Claude Code 工作流",
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
                "topic": "深度学习 / Transformer 论文精读",
                "goal": "拆开自注意力、QKV、多头注意力、编码器解码器和位置编码。",
            },
            {
                "topic": "LoRA 论文精读",
                "goal": "理解 PEFT、低秩更新和 LoRA 放进 Transformer 的方式。",
            },
            {
                "topic": "大语言模型 / 李宏毅 LLM 课程",
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
    {
        "id": "model-foundations-training",
        "title": "模型底层与训练线",
        "subtitle": "从小语言模型训练闭环走到数据工程、后训练和推理模型训练。",
        "audience": "适合已经会用模型，想理解模型能力如何被数据和训练塑形的人。",
        "outcome": "完成后应能把 tokenizer、数据、训练系统、后训练和工具使用训练串成一条模型能力生产线。",
        "stages": [
            {
                "topic": "大语言模型 / 从零训练小语言模型",
                "goal": "先跑通从数据到训练再到评测的最小语言模型闭环。",
            },
            {
                "topic": "大语言模型 / 预训练数据工程与数据配方",
                "goal": "理解数据清洗、质量过滤和混合比例为什么决定模型底色。",
            },
            {
                "topic": "大语言模型 / 后训练全栈",
                "goal": "区分 SFT、偏好优化和 RLHF 如何改变模型行为。",
            },
            {
                "topic": "大语言模型 / 推理模型训练",
                "goal": "理解可验证奖励、GRPO 和蒸馏如何训练推理能力。",
            },
            {
                "topic": "大语言模型 / Agentic 后训练与工具使用 RL",
                "goal": "把模型训练接到工具、搜索和环境交互任务上。",
            },
        ],
    },
    {
        "id": "ai-infra",
        "title": "AI 基础设施线",
        "subtitle": "从 GPU 性能走到推理引擎、分布式训练和 LLM Serving。",
        "audience": "适合想知道模型为什么跑得慢、为什么贵、怎样稳定上线的人。",
        "outcome": "完成后应能解释 LLM 系统的计算、显存、并发、调度和服务边界。",
        "stages": [
            {
                "topic": "AI 基础设施 / GPU 性能工程",
                "goal": "建立 GPU 执行模型、kernel 和 profiling 的基本判断力。",
            },
            {
                "topic": "AI 基础设施 / 现代 LLM 推理引擎内核",
                "goal": "理解 KV cache、PagedAttention、连续批处理和调度如何影响吞吐。",
            },
            {
                "topic": "AI 基础设施 / 分布式训练系统",
                "goal": "拆开 sharding、并行策略和通信，让大模型训练系统不再是黑箱。",
            },
            {
                "topic": "AI 基础设施 / LLM Serving 架构与请求调度",
                "goal": "把推理引擎接进可上线服务，处理路由、限流、缓存、监控和成本。",
            },
        ],
    },
    {
        "id": "agent-reliable-systems",
        "title": "Agent 可靠系统线",
        "subtitle": "从 Agent 基础走到执行外壳、工具契约和可恢复可靠性。",
        "audience": "适合已经做过 Agent demo，想把它变成可诊断、可恢复系统的人。",
        "outcome": "完成后应能设计一个有工具接口、状态恢复、评测和执行溯源的 Agent 系统。",
        "stages": [
            {
                "topic": "Agent / Agent 基础与工程",
                "goal": "先确认 Agent Loop、工具调用、状态和评测的基本概念。",
            },
            {
                "topic": "Agent / Agent Harness Engineering",
                "goal": "把 Agent 放进可运行外壳，处理权限、沙箱、重试和恢复。",
            },
            {
                "topic": "Agent / 工具调用契约与结构化交互",
                "goal": "把工具 schema、结构化输出和错误策略做成稳定接口。",
            },
            {
                "topic": "Agent / Agent 可靠性工程",
                "goal": "用 durable execution、Tracing 和回归评测让长程任务可验收。",
            },
        ],
    },
]

STATIC_COURSES = [
    {
        "id": "context-engineering",
        "topic": "Agent / Context Engineering",
        "title": COURSE_PROFILES["Agent / Context Engineering"]["title"],
        "summary": COURSE_PROFILES["Agent / Context Engineering"]["summary"],
        "audience": COURSE_PROFILES["Agent / Context Engineering"]["audience"],
        "firstStep": COURSE_PROFILES["Agent / Context Engineering"]["firstStep"],
        "outcome": COURSE_PROFILES["Agent / Context Engineering"]["outcome"],
        "level": COURSE_PROFILES["Agent / Context Engineering"]["level"],
        "status": COURSE_PROFILES["Agent / Context Engineering"]["status"],
        "pageCount": 4,
        "entryPath": "Agent/研习资料/Context Engineering/index.html",
        "tags": ["Agent", "Context Engineering"],
        "pages": [
            {
                "topic": "Agent / Context Engineering",
                "title": "01 从 Prompt 到 Context：为什么 Agent 需要上下文工程",
                "path": "Agent/研习资料/Context Engineering/01_从 Prompt 到 Context：为什么 Agent 需要上下文工程.html",
                "tags": ["Agent", "Context Engineering"],
            },
            {
                "topic": "Agent / Context Engineering",
                "title": "02 上下文控制面：State、Store、Runtime 与 Middleware",
                "path": "Agent/研习资料/Context Engineering/02_上下文控制面：State、Store、Runtime 与 Middleware.html",
                "tags": ["Agent", "Context Engineering"],
            },
            {
                "topic": "Agent / Context Engineering",
                "title": "03 四类策略：Write、Select、Compress、Isolate",
                "path": "Agent/研习资料/Context Engineering/03_四类策略：Write、Select、Compress、Isolate.html",
                "tags": ["Agent", "Context Engineering"],
            },
            {
                "topic": "Agent / Context Engineering",
                "title": "04 产品案例与工程验收：Claude Code、Manus、Kiro",
                "path": "Agent/研习资料/Context Engineering/04_产品案例与工程验收：Claude Code、Manus、Kiro.html",
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
            static_topics.add(str(static_course["topic"]))

    for public_course in PUBLIC_COURSES:
        topic = str(public_course["topic"])
        if topic in static_topics:
            continue
        root = str(public_course["root"])
        root_path = ROOT / root
        index_path = f"{root}/index.html"
        if not (root_path / "index.html").exists():
            continue
        profile = COURSE_PROFILES.get(topic, {})
        courses.append(
            {
                "id": slugify(topic),
                "topic": topic,
                "title": profile.get("title", topic),
                "summary": profile.get("summary", ""),
                "audience": profile.get("audience", ""),
                "firstStep": profile.get("firstStep", "先读课程地图。"),
                "outcome": profile.get("outcome", ""),
                "level": profile.get("level", ""),
                "status": profile.get("status", "planned"),
                "pageCount": 0,
                "courseRoot": root,
                "indexPath": index_path,
                "entryPath": index_path,
                "firstPagePath": "",
                "tags": public_course.get("tags", []),
            }
        )

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
            course = courses_by_topic.get(topic, {})
            if not stage_pages and not course:
                print(f"skip missing stage: {topic}")
                continue
            first_page = stage_pages[0] if stage_pages else None
            profile = COURSE_PROFILES.get(topic, {})
            stages.append(
                {
                    "order": index,
                    "topic": topic,
                    "title": course.get("title", profile.get("title", topic)),
                    "goal": stage["goal"],
                    "pageCount": len(stage_pages),
                    "entryPath": course.get("entryPath", first_page["path"] if first_page else ""),
                    "entryTitle": first_page["title"] if first_page else "课程地图",
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
        "planned": "已建地图",
    }
    return labels.get(str(status), str(status) if status else "可学习")


def unit_intent(index: int, total: int, title: str) -> str:
    if re.search(r"作业|练习|HW|Bonus", title, re.IGNORECASE):
        return "把前面的概念压到可提交、可检查的任务里，确认自己不是只会复述。"
    if re.search(r"总览|概览|导览|课程说明|README", title, re.IGNORECASE):
        return "先建立本课程的范围、问题意识和阅读顺序，避免后面只是在扫术语。"
    if total == 1:
        return "作为这个专题的独立学习入口，用来建立核心概念、例子和判断边界。"
    if index == 1:
        return "建立本课程的第一层直觉和共同词表，后续小节都默认已经理解这一层。"
    if index == total:
        return "收束全课，把前面的概念迁移到更完整的案例、边界或后续学习方向。"
    if index <= max(2, total // 3):
        return "补上主线基础，让后面的结构、公式、工程或案例有落点。"
    if index <= max(3, (total * 2) // 3):
        return "把基础概念推进到可操作层，开始处理组合、实现和常见误区。"
    return "处理进阶情形、验证方式和迁移边界，帮助把知识从会看变成会用。"


def phase_label(order: int) -> str:
    labels = ["建立入口", "核心机制", "工程展开", "边界验证", "延伸迁移"]
    if order <= len(labels):
        return labels[order - 1]
    return f"阶段 {order}"


def phase_summary(order: int) -> str:
    summaries = [
        "先抓住课程讨论的对象、基本问题和必要词表。",
        "进入关键结构和方法，理解它们分别解决什么问题。",
        "把方法放进案例、流程或代码里，观察真实约束。",
        "检查评估、安全、失败模式、成本或可解释性等边界。",
        "把本课知识接到相邻课程、论文、项目或练习里。",
    ]
    if order <= len(summaries):
        return summaries[order - 1]
    return "继续按顺序学习，保留前后章节之间的依赖关系。"


def build_phase_cards(pages: list[dict[str, object]]) -> str:
    total = len(pages)
    if total <= 3:
        group_count = 1
    elif total <= 8:
        group_count = 2
    elif total <= 20:
        group_count = 3
    else:
        group_count = 5

    size = max(1, (total + group_count - 1) // group_count)
    cards = []
    for group_index, start in enumerate(range(0, total, size), start=1):
        chunk = pages[start : start + size]
        if not chunk:
            continue
        first = start + 1
        last = start + len(chunk)
        titles = " / ".join(str(page["title"]) for page in chunk[:3])
        if len(chunk) > 3:
            titles += " / ..."
        cards.append(
            f"""
          <div class="flow-card">
            <b>{first:02d}-{last:02d}｜{html.escape(phase_label(group_index))}</b>
            <p>{html.escape(phase_summary(group_index))}</p>
            <small>{html.escape(titles)}</small>
          </div>"""
        )
    return "\n".join(cards)


def after_learning_text(topic: str) -> str:
    if "Agent" in topic:
        return "学完后建议回到 Agent 学习地图，按需要继续接 Context Engineering、Claude Code 工作流、多智能体系统，或转到大语言模型方向补 Harness Engineering 与 MCP。"
    if "大语言模型" in topic or "LLM" in topic or "LoRA" in topic or "RAG" in topic:
        return "学完后可以按目标分流：做应用就接 Agent 学习地图，补模型结构就接 Transformer，做微调就继续 LoRA 或长线 LLM 课程。"
    if "深度学习" in topic or "PyTorch" in topic:
        return "学完后可以继续 Transformer 论文精读、大语言模型学习地图，或回到 PyTorch 项目里跑完整训练闭环。"
    if "算法" in topic:
        return "学完后回到算法学习地图，继续下一组题型；做面试准备时优先把模板写成可复用代码。"
    return "学完后回到研究总图，根据目标选择相邻课程；不要把本课程当成孤立清单。"


def related_links(index_path: str, topic: str) -> str:
    links = [("研究总图", "index.html")]
    if "大语言模型" in topic or "LLM" in topic or "LoRA" in topic or "RAG" in topic:
        links.append(("大语言模型学习地图", "大语言模型/研习资料/index.html"))
        links.append(("Agent 学习地图", "Agent/研习资料/index.html"))
    if "Agent" in topic:
        links.append(("Agent 学习地图", "Agent/研习资料/index.html"))
        links.append(("大语言模型学习地图", "大语言模型/研习资料/index.html"))
    if "深度学习" in topic or "PyTorch" in topic:
        links.append(("深度学习学习地图", "深度学习/研习资料/index.html"))
        links.append(("大语言模型学习地图", "大语言模型/研习资料/index.html"))
    if "算法" in topic:
        links.append(("算法学习地图", "算法/研习资料/index.html"))

    seen = set()
    html_links = []
    for label, target in links:
        if target in seen:
            continue
        seen.add(target)
        html_links.append(f'<a href="{href_from(index_path, target)}">{html.escape(label)}</a>')
    return "\n".join(html_links)


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
        intent = html.escape(unit_intent(index, len(pages), str(page["title"])))
        page_cards.append(
            f"""
          <article class="unit" id="unit-{index:02d}">
            <div class="unit-number">{index:02d}</div>
            <div>
              <h3>{page_title}</h3>
              <p><b>制作意图：</b>{intent}</p>
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
    phases_html = build_phase_cards(pages)
    after_text = html.escape(after_learning_text(topic))
    related_html = related_links(index_path, topic)

    return f"""<!doctype html>
<html lang="zh-CN" data-page-shell="index-page-v1">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}｜课程地图</title>
  <meta name="description" content="{html.escape(summary)}">
  <style>
    :root {{
      --bg:#d8d4cc;--paper:#fbfaf6;--paper-2:#eee7d9;--ink:#24221f;--muted:#67645d;
      --line:rgba(36,34,31,.18);--rail:#232320;--panel:rgba(251,250,246,.97);--panel-2:#f8f3e7;
      --accent:#216d5d;--green:#216d5d;--red:#a9473d;--lime:#d7ef66;
      --shadow:0 14px 28px rgba(60,56,48,.10);
      --mono:"Cascadia Code","SFMono-Regular",Consolas,monospace;
      --sans:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;
      --serif:"Songti SC","Noto Serif CJK SC",SimSun,serif;
    }}
    *{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
    body{{margin:0;min-height:100vh;color:var(--ink);font-family:var(--sans);line-height:1.76;background:
      linear-gradient(90deg,rgba(17,17,17,.035) 1px,transparent 1px) 0 0/72px 72px,
      linear-gradient(rgba(17,17,17,.03) 1px,transparent 1px) 0 0/72px 72px,var(--bg)}}
    a{{color:inherit}}.layout{{display:grid;grid-template-columns:284px minmax(0,1fr);min-height:100vh}}
    aside{{position:sticky;top:0;height:100vh;overflow:auto;padding:24px 17px;color:#f4f0e8;border-right:1px solid rgba(255,255,255,.12);background:var(--rail)}}
    .mark{{display:inline-grid;place-items:center;width:42px;height:42px;margin-bottom:16px;background:rgba(255,255,255,.08);border:1px solid rgba(226,222,218,.22);color:var(--lime);font-family:var(--mono);font-weight:800}}
    h1{{margin:0;font-family:var(--serif);font-size:32px;line-height:1.08;letter-spacing:0}}.subtitle{{margin:14px 0 0;color:#c9c3b7;font-size:13px}}
    .side-label{{display:block;margin:22px 0 7px;color:#c9c3b7;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase}}
    .path-nav{{display:grid;gap:5px}}.path-nav a{{display:grid;grid-template-columns:42px minmax(0,1fr);gap:8px;align-items:center;padding:8px 10px;border:1px solid transparent;border-radius:6px;color:#eee9dd;text-decoration:none;font-size:13px}}
    .path-nav a:hover{{background:rgba(255,255,255,.075);border-color:rgba(255,255,255,.16)}}.path-nav span{{font-family:var(--mono);color:var(--lime);font-weight:800}}
    main{{min-width:0;width:100%;padding:30px 38px 64px}}.hero{{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,420px);gap:28px;align-items:end;padding:30px;border:1px solid var(--line);border-left:6px solid var(--ink);border-top:0;border-radius:8px;background:linear-gradient(90deg,rgba(36,34,31,.025) 1px,transparent 1px),linear-gradient(rgba(36,34,31,.022) 1px,transparent 1px),var(--panel);background-size:32px 32px;box-shadow:var(--shadow)}}
    .kicker{{width:max-content;max-width:100%;padding:4px 8px;color:var(--accent);font-family:var(--mono);font-size:11px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}}
    .hero h2{{margin:18px 0 0;font-family:var(--serif);font-size:clamp(34px,5vw,52px);line-height:1.12;letter-spacing:0}}
    .hero-copy{{color:var(--muted);font-size:16px}}.hero-copy a{{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(29,95,143,.35)}}
    .chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}}.chip{{display:inline-flex;align-items:center;min-height:26px;padding:3px 8px;border:1px solid var(--line);background:var(--panel);color:var(--muted);font-size:12px}}.chip.strong{{border-color:var(--ink);color:var(--ink);font-family:var(--mono)}}
    .panel{{margin-top:14px;border:1px solid var(--line);border-radius:8px;background:var(--panel);box-shadow:var(--shadow)}}.panel-head{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;padding:22px 24px;border-bottom:1px solid var(--line);background:transparent}}
    .panel-head h2{{margin:0;font-family:var(--serif);font-size:clamp(26px,4vw,40px);line-height:1.12}}.panel-head p{{margin:8px 0 0;color:var(--muted)}}.count{{padding:4px 8px;border:1px solid var(--line);background:var(--paper-2);color:var(--muted);font-family:var(--mono);font-size:12px;white-space:nowrap}}
    .meta-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line)}}.meta{{padding:18px;background:var(--panel)}}.meta b{{display:block;margin-bottom:8px;font-family:var(--mono);font-size:12px;color:var(--green);letter-spacing:.08em}}.meta p{{margin:0;color:var(--muted)}}
    .flow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1px;background:var(--line)}}.flow-card{{min-height:172px;padding:18px;background:var(--panel)}}.flow-card b{{display:block;color:var(--red);font-family:var(--mono);font-size:12px;letter-spacing:.06em}}.flow-card p{{margin:10px 0 0;color:var(--muted)}}.flow-card small{{display:block;margin-top:12px;color:var(--muted);font-size:12px}}
    .bridge{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line)}}.bridge div{{padding:18px;background:rgba(255,255,255,.56)}}.bridge b{{display:block;margin-bottom:8px;color:var(--green);font-family:var(--mono);font-size:12px;letter-spacing:.08em}}.bridge p{{margin:0;color:var(--muted)}}.bridge a{{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(33,109,93,.35)}}.related{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}.related a{{display:inline-flex;align-items:center;min-height:30px;padding:5px 9px;border:1px solid var(--line);background:rgba(255,255,255,.68);text-decoration:none;color:var(--ink);font-weight:700}}.related a:hover{{border-color:var(--accent);color:var(--accent)}}
    .units{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1px;background:var(--line)}}.unit{{display:grid;grid-template-rows:auto 1fr auto;min-height:220px;padding:18px;background:var(--panel)}}
    .unit-number{{font-family:var(--mono);font-size:13px;color:var(--red);font-weight:800}}.unit h3{{margin:12px 0 0;font-size:20px;line-height:1.28}}.unit p{{margin:10px 0 0;color:var(--muted);font-size:13px}}.unit a,.primary{{display:inline-flex;align-items:center;justify-content:center;min-height:36px;margin-top:16px;padding:7px 10px;border:1px solid var(--ink);background:var(--ink);color:#fff;text-decoration:none;font-size:13px;font-weight:700}}.unit a:hover,.primary:hover{{background:var(--accent);border-color:var(--accent)}}
    @media(max-width:900px){{.layout{{grid-template-columns:1fr}}aside{{position:static;height:auto}}.hero,.meta-grid,.bridge{{grid-template-columns:1fr}}main{{padding:24px 16px 44px}}.hero h2{{font-size:38px}}}}
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
            <h2>课程总论</h2>
            <p>这页先锁定课程边界，再进入具体小节。</p>
          </div>
          <span class="count">{html.escape(str(len(pages)))} 小节</span>
        </div>
        <div class="meta-grid">
          <div class="meta"><b>适合对象</b><p>{html.escape(audience)}</p></div>
          <div class="meta"><b>学完能做</b><p>{html.escape(outcome)}</p></div>
          <div class="meta"><b>课程位置</b><p>{html.escape(topic)}</p></div>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <h2>知识导图</h2>
            <p>按阶段看这门课，而不是把小节当成孤立链接。</p>
          </div>
          <span class="count">Map</span>
        </div>
        <div class="flow">
          {phases_html}
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <h2>前置与衔接</h2>
            <p>每门课都要说明从哪里来、先做什么、学完去哪里。</p>
          </div>
          <span class="count">Context</span>
        </div>
        <div class="bridge">
          <div><b>前置知识</b><p>{html.escape(audience)}</p></div>
          <div><b>推荐起点</b><p>{html.escape(first_step)}</p></div>
          <div><b>后续推荐</b><p>{after_text}</p><div class="related">{related_html}</div></div>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <h2>全部小节</h2>
            <p>每个入口都说明本单元在课程里的制作意图。</p>
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
        if str(course.get("courseRoot", "")) in PRESERVE_COURSE_INDEX_ROOTS:
            continue
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
        if str(course.get("courseRoot", "")) in PRESERVE_COURSE_INDEX_ROOTS:
            continue
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
