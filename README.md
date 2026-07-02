# AI Study Lab

这是一个公开的中文 AI 学习资料库，以大语言模型、Agent、深度学习、算法和工程实践为核心方向。资料以 **v2 风格 HTML 学习页** 形式组织，白色背景、顶部导航、卡片网格，适合在 GitHub Pages 上阅读和导航。

站点入口：[AI Study Lab](https://fewiyuu.github.io/ai-study-lab/)

## 内容范围

- **大语言模型**：基础与应用工程、RAG、MCP、Harness Engineering、LoRA、从零训练
- **Agent**：基础与工程、Agent Skills、Context Engineering、Claude Code 工作流、多智能体系统、Harness 与可靠性
- **深度学习**：PyTorch 实践、Transformer、CNN、RNN、训练闭环
- **算法**：数组链表、树堆图、回溯、动态规划、面试题型
- **工程基础**：MIT Missing Semester（命令行、Git、调试、安全、构建自动化）
- **AI 基础设施**：GPU 性能工程、LLM 推理引擎、Serving 架构、分布式训练系统

这些内容更像一间持续整理中的学习实验室：强调可读、可复用、可继续迭代，不把它包装成完整教材或权威文档。

## 推荐入口

| 入口 | 说明 |
|------|------|
| [网站首页](https://fewiyuu.github.io/ai-study-lab/) | 学习路径、课程选读、全站搜索 |
| [大语言模型学习地图](https://fewiyuu.github.io/ai-study-lab/大语言模型/研习资料/index.html) | LLM 基础、RAG、MCP、Harness、LoRA、训练 |
| [Agent 学习地图](https://fewiyuu.github.io/ai-study-lab/Agent/研习资料/index.html) | Agent 基础、Skills、Context Engineering、多智能体 |
| [深度学习学习地图](https://fewiyuu.github.io/ai-study-lab/深度学习/研习资料/index.html) | PyTorch、Transformer、CNN、RNN |
| [算法学习地图](https://fewiyuu.github.io/ai-study-lab/算法/研习资料/index.html) | 数据结构、算法题型、面试准备 |
| [PyTorch 深度学习实践](https://fewiyuu.github.io/ai-study-lab/PyTorch深度学习实践%20刘二大人/研习资料/index.html) | 刘二大人课程精读 |
| [李宏毅机器学习](https://fewiyuu.github.io/ai-study-lab/李宏毅%20%20机器学习/研习资料/index.html) | 58 讲完整课程 |
| [工程基本功](https://fewiyuu.github.io/ai-study-lab/计算机教育中缺失的一课/研习资料/index.html) | MIT Missing Semester |
| [AI 基础设施](https://fewiyuu.github.io/ai-study-lab/AI基础设施/研习资料/index.html) | GPU、推理引擎、Serving、分布式训练 |
| [岗位地图](https://fewiyuu.github.io/ai-study-lab/jobs.html) | AI 相关岗位方向与能力要求 |

页面层级：首页 → 课程索引 → 子课程索引 → 单元学习页。每级都有面包屑导航和返回链接。

## 使用说明

- **不知道从哪开始**：打开网站首页，先看"学习路径"，再选一门感兴趣的课进入课程索引。
- **已有明确方向**：直接在首页"课程选读"卡片里挑一门课，进入课程索引后选子课程，再选具体单元。
- **搜索**：使用顶部导航栏的搜索按钮，或打开 `search.html` 直接搜索全站内容。
- **HTML 学习页**：建议通过 GitHub Pages 阅读，排版和交互体验更稳定（支持 KaTeX 公式、Prism 代码高亮、练习交互）。
- **Markdown 笔记**：可以直接在 GitHub 阅读，也可以下载后放入自己的笔记工具继续整理。
- **内容以中文为主**：英文术语会尽量保留原文，方便继续查阅官方资料。
- **部分目录仍在整理中**：链接、标题和入口会随学习进度迭代。

## 项目结构

```
ai-study-lab/
├── index.html              # 网站首页：课程地图 + 学习路径
├── search.html             # 全站搜索页
├── jobs.html               # AI 岗位地图
├── catalog.json            # 公开目录数据（搜索索引源）
├── assets/
│   ├── site-v2.css         # 站点级共享样式（导航、卡片、单元列表）
│   ├── study-page-v2.css   # 学习页样式（KaTeX、Prism、练习）
│   ├── study-page-v2.js    # 学习页交互（练习、导出、目录）
│   ├── search-index.json   # 搜索索引数据
│   └── vendor/             # KaTeX、Prism 等第三方库
├── scripts/
│   ├── md-to-study-page.py      # Markdown → HTML 学习页转换器
│   ├── build_catalog.py         # 生成 catalog.json（默认不生成索引页）
│   ├── build-search-index.py    # 生成搜索索引
│   ├── gen-course-index.py      # 生成课程索引页
│   ├── rewrite-subcourse-index.py # 重写子课程索引页
│   └── html-to-study-md.py      # HTML → Markdown 反向转换器
├── 大语言模型/             # 课程专题
│   ├── 研习资料/
│   │   ├── index.html      # 课程索引页
│   │   ├── LLM基础与应用工程/
│   │   │   ├── index.html  # 子课程索引页
│   │   │   └── 01_单元名/
│   │   │       └── 学习页.html
│   │   └── ...其他子课程/
│   └── 笔记/
├── Agent/                  # 同上结构
├── 深度学习/
├── 算法/
├── PyTorch深度学习实践 刘二大人/
├── 李宏毅  机器学习/
├── 计算机教育中缺失的一课/
├── AI基础设施/
└── projects/               # 项目实践
    └── index.html
```

## 生成流程

资料由 Markdown 源文件生成 HTML 学习页，再由脚本生成索引和搜索数据：

1. **Markdown → HTML**：`python scripts/md-to-study-page.py --batch 课程/研习资料/子课程/单元/`
2. **更新目录**：`python scripts/build_catalog.py`（只生成 `catalog.json`，不覆盖索引页）
3. **更新课程索引**：`python scripts/gen-course-index.py`
4. **更新子课程索引**：`python scripts/rewrite-subcourse-index.py`
5. **更新搜索索引**：`python scripts/build-search-index.py`

## 隐私与发布边界

这个仓库只发布适合公开阅读的学习资料。

不会包含：

- 个人日记、收件箱、内部计划或私人复盘
- 账号、密钥、配置、聊天记录等敏感信息
- 未公开项目材料、商业资料或他人隐私内容

如果发现上述内容误入仓库，欢迎通过 Issue 提醒，我会优先处理。

## 说明

本仓库主要用于个人学习沉淀和公开分享。内容会尽量标注来源和上下文，但仍可能存在理解偏差、过期信息或尚未补完的章节；正式使用前请结合原始资料自行核对。
