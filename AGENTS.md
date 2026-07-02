# ai-study-lab 协作指南

**生成日期**: 2026年7月2日
**最后更新**: 2026年7月2日

---

## 协作目标

这个仓库是一个 **纯静态站点**，托管在 GitHub Pages 上，用于公开发布 AI、Agent、深度学习、算法和工程实践相关的中文学习资料。

Codex 在这个仓库中的默认任务：
- 维护公开学习资料、GitHub Pages 网站入口、README、导航和链接
- 将 Markdown 学习笔记转换为 HTML 学习页
- 维护课程索引页（v2 风格：白色背景 + 顶部导航 + 卡片网格）
- 维护站点级共享样式和搜索功能
- 确保新增内容能从公开导航进入，链接正确、标题合理

## 站点架构（v2 风格）

站点采用统一 v2 视觉风格：白色背景、Inter 字体、顶部 sticky 导航、卡片网格布局。

页面层级：
```
根目录 index.html         → 课程地图（8 门课程卡片 + 学习路径）
  ↓
课程/研习资料/index.html   → 课程索引（子课程卡片 + 单元列表）
  ↓
子课程/index.html          → 子课程索引（单元列表）
  ↓
单元/学习页.html           → 具体学习页（KaTeX + Prism + 练习交互）
```

根目录还有：
- `search.html` — 全站搜索页
- `jobs.html` — AI 岗位地图
- `projects/index.html` — 项目实践页

## 维护边界

### 优先维护

- `README.md`：公开仓库入口说明
- `index.html`、`search.html`、`jobs.html`：站点根入口
- `catalog.json`、`assets/search-index.json`：目录数据和搜索索引
- `assets/site-v2.css`、`assets/study-page-v2.css`：站点共享样式和学习页样式
- 各专题 `研习资料/index.html`：课程索引页（v2 风格）
- 各子课程 `index.html`：子课程索引页（v2 风格）
- 各单元 `学习页.html`：由 Markdown 转换而来的 HTML 学习页

### 不处理

- 个人日记、收件箱、主页、个人项目推进等内部内容
- 不属于本仓库的私有工作流文件
- 账号信息、隐私材料、未公开项目资料、敏感配置
- 旧版 v1 文件（已删除，不要恢复）

## 内容组织

新增或整理公开资料时，优先沿用现有结构：

- 专题目录：如 `大语言模型/`、`Agent/`、`算法/`、`深度学习/`、`PyTorch深度学习实践 刘二大人/`、`李宏毅  机器学习/`、`计算机教育中缺失的一课/`、`AI基础设施/`
- 学习页：优先放在对应专题的 `研习资料/子课程/单元/学习页.html`
- 原始 Markdown：放在对应专题的 `笔记/`
- 课程入口：优先维护 `研习资料/index.html`（v2 风格课程索引页）

大量新增学习页时，同步检查：
- `README.md` 是否仍准确描述仓库内容
- 对应专题的 `研习资料/index.html` 是否包含新课程/子课程
- 子课程 `index.html` 是否包含新单元
- 上一级导航入口是否能让读者找到新内容
- `assets/search-index.json` 是否需要重新生成

## 构建流程

### Markdown → HTML 学习页

```bash
python scripts/md-to-study-page.py --batch --overwrite 课程/研习资料/子课程/单元/
```

由 `md-to-study-page.py` 将 Markdown 学习笔记转换为 v2 风格 HTML 学习页。模板引用 `assets/study-page-v2.css` 和 `assets/study-page-v2.js`。

### 生成目录数据

```bash
python scripts/build_catalog.py
```

默认**只生成 `catalog.json`**，不覆盖任何索引页。如果确实需要生成旧版 v1 索引页（一般不推荐）：

```bash
python scripts/build_catalog.py --write-indexes
```

### 生成课程索引页

```bash
python scripts/gen-course-index.py
```

生成 8 门课程的 `研习资料/index.html`（v2 风格）。

### 重写子课程索引页

```bash
python scripts/rewrite-subcourse-index.py
```

遍历所有子课程目录，重写 `index.html` 为 v2 风格。

### 生成搜索索引

```bash
python scripts/build-search-index.py
```

从 `catalog.json` 读取公开页面列表，生成 `assets/search-index.json`，供 `search.html` 使用。

## 旧版清理

以下文件/目录已删除，不要再恢复：

- `study-page.css`、`study-page.js` → 替换为 `study-page-v2.css`、`study-page-v2.js`
- `index-page.css` → 样式已并入 `site-v2.css`
- `mkdocs.yml`、`convert_to_mkdocs.py`、`sync_mkdocs.py` → 不再使用 MkDocs
- `docs/` → 旧版 MkDocs 构建输出
- `course-shell.json`、`build_course_shell.py` → 导航工具已废弃
- `demo-lesson-layout-v2.html` → 测试文件
- `scripts/__pycache__/` → 纯运行时缓存

## 写作与链接规范

- 始终使用中文回答和维护文档，必要时保留英文术语
- 内容面向公开读者，避免只对 Vault 本人可理解的上下文
- 标题要清晰、可检索、可作为导航文本
- 外部链接使用标准 Markdown 链接
- 学习页内链使用相对路径（如 `../index.html`）
- 不使用本机绝对路径作为公开链接
- 对来源、日期、课程名、论文名和版本信息尽量写清楚

## v2 风格约定

- 新增/修改索引页时，统一使用 v2 风格（`site-v2.css`）
- 不要恢复或创建旧版 v1 风格页面（侧边栏 + 暖色背景）
- 学习页统一使用 `study-page-v2.css` 模板
- 索引页统一使用 `site-v2.css` 中的 `.card-grid`、`.unit-list`、`.top-nav` 等组件
- 如果运行 `build_catalog.py`，不要加 `--write-indexes`，避免覆盖 v2 索引页

## 发布质量检查

发布或准备发布前，至少检查：

- README 是否说明仓库定位、主要入口和学习路径
- 新增页面是否能从公开导航进入（从根目录 → 课程索引 → 子课程索引 → 学习页）
- HTML 链接、CSS 引用、JS 引用是否可用
- 是否误包含私有 Vault 链接、日记、收件箱、个人账号或敏感信息
- GitHub Pages 入口页面是否能正常打开、标题是否合理、移动端是否基本可读
- 搜索索引 `assets/search-index.json` 是否已同步更新

如果涉及页面视觉或交互改动，启动本地预览或用浏览器实际打开检查。

## 工具偏好

- 查找文件和文本优先用 `rg` / `rg --files`
- Python 包管理统一使用 `uv`
- 高噪声 CLI 输出优先用 `chop` 压缩
- 不为了小改动扫描整个仓库；先定位，再读取必要文件

## Git 约定

- 默认只做本地修改
- 不提交、不推送，除非用户明确要求
- 推送或发布前，先说明本地变更、远程差异和预期影响
- 遇到已有未提交改动，先保护用户改动，不擅自回滚
