# 02_KV_cache与显存账本｜Local Source Pack

## Source Boundary

- Course map: `../index.html`
- Current unit draft: `学习页.html`，最后修改时间 2026-06-09 18:38
- Public source names already出现在旧页里：vLLM 文档、PagedAttention 论文、SGLang 文档
- Rebuild date: 2026-06-20

## Source-To-Unit Notes

- 课程地图决定单元顺序：01 先讲 prefill / decode，02 讲 KV cache 账本，03 再讲 PagedAttention 块管理。
- 旧页已经给出了这单元的核心骨架：KV cache 公式、显存账本、prefix cache、GQA 影响、HiCache 分层、OOM 诊断、练习与导出。
- 重构时要保留的内容：`KV bytes/token` 公式、32 层 / 32 KV heads / head dim 128 / BF16 的算例、8 KV heads 的 GQA 对比、prefix cache 与 PagedAttention 的分工、KV 量化的字节层收益。
- 重构时要改掉的内容：旧式整页自定义壳、重复收束句、带有内部流程感的元叙述、与课程 shell 不一致的导航结构。

## Operational Facts

- 旧页锚定算例：32 层、32 个 KV heads、head dim 128、BF16、4096 tokens、4 个活跃请求。
- GQA 对比算例：同样层数和 head dim，但 KV heads 降到 8。
- 旧页给出的数值直觉：4096 tokens、32 KV heads 时，单请求 KV cache 约 2 GiB；4096 tokens、8 KV heads 时，单请求 KV cache 约 512 MiB。
- 本单元的核心判断不是“模型能不能加载”，而是“权重、KV cache、块浪费、输出长度和运行时开销加起来能不能稳态服务”。

## Gaps

- 没有额外爬网；当前重构只依赖本地课程地图和旧页。
- 旧页没有记录上游仓库版本号或发布 hash；涉及会变动的工程事实时，应按当前课程地图和本地算例来教，不要伪装成冻结版本。
- 这页只负责 KV cache 账本和相邻优化的边界说明，PagedAttention 的块分配细节留给下一单元。
