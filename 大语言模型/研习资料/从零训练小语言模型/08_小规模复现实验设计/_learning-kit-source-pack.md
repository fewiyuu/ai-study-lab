# Source Pack: 小规模复现实验设计

## Source Boundary

- Course: 从零训练小语言模型
- Unit: 08 小规模复现实验设计
- Snapshot: 2026-06-21
- Access date: 2026-06-21
- Local inputs: course-root `index.html`、当前单元页 `学习页.html`、以及相邻单元 07 / 06 的页面和课程壳。

## Source-To-Unit Notes

- 课程索引把本单元放在 `从教学代码到开放训练配方` 之后、`从零训练小语言模型` 主线的收尾位置，所以这一页要把前面的判断方法收束成一份可执行、可停机、可复盘的实验计划。
- 当前单元页已经把教学目标定得很清楚：把一个小规模复现实验写成问题、预算、数据、模型、指标、停机线和边界说明，而不是只留下一个配置片段。
- 公开来源标签沿用当前页已经出现的来源名：`Stanford CS336: Language Modeling from Scratch`、`OLMo 2` 论文与项目页、`Scaling Laws for Neural Language Models`、`Training Compute-Optimal Large Language Models`、`Holistic Evaluation of Language Models`、`Language Models are Few-Shot Learners`、`An Open Source Data Contamination Report for Large Language Models`、`Paloma`，以及 PyTorch / NVIDIA / NCCL / Triton 的公开文档。
- 这些来源只支撑本页的公共边界：如何写小规模复现实验计划，如何估预算，如何分清主指标与诊断指标，如何先写停机线，再谈外推。

## Unit Boundary

- 本页覆盖：实验问题句、预算估算、数据与模型账本、最小案例、预算算例、案例对照、停机与错误、以及从 07 页带来的字段如何落到 08 页。
- 本页不覆盖：完整 benchmark 实现、数据清洗流水线细节、完整 scaling fit、后训练配方和大规模系统优化。这些内容留给相邻或后续单元。
- 这页的锚点应该停在“小计划如何写得可执行、可回查”，不要扩成论文综述、仓库说明或发布材料。

## Gaps

- 没有提供本地仓库快照、benchmark 日志或私有实现说明，所以不要在这一页里写出具体仓库文件名、测试名、数值结果或 checkpoint 数量。
- 不要把示例预算、吞吐和成本当作真实结论；它们只用来教学和校准数量级。
- 如果后续单元需要更具体的仓库命令、文件路径或失败模式，再为那个单元单独建 source pack，不要把这页的边界拉宽。
