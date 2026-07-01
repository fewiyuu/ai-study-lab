# P10_验证集过拟合 本地 Source Pack

## Source Boundary

- 课程目录页：`../index.html`
  - 用来确认 P10 在整门课里的位置，承接 P09，连接 P11。
- 旧版 P10 学习页：`学习页.html`
  - 用来提取这一节已经覆盖的主线、例子、代码和常见误区。
- 课程说明：`../README.md`
  - 用来确认整门课程的命名方式和课程页的统一写法。

Snapshot: 本地文件于 2026-06-21 检查。

## Source-To-Unit Notes

- 这节课在整门课里承接 P09 的结构性建模，转向“模型已经选出来以后，怎么确认它没有被验证集带偏”。
- 旧页的主线已经很清楚：
  - training set 用来学参数。
  - validation set 用来选模型和超参数。
  - test set 用来做最终评估。
  - 如果把同一个 validation set 反复拿来试很多模型，validation 本身也会被过拟合。
  - 可以把这一过程写成 `H_val`：候选模型集合越大，越容易挑到只讨好 validation 的模型。
  - 公开 leaderboard 也会变成一种被反复优化的 validation set。
  - 更稳的做法是预先限制搜索空间、保留最终 test、记录试验次数、用多 seed 或交叉验证看波动。
  - 代码桥接已经出现过：`best_id = argmin(val_losses)` 说明 validation 是在做选择，不是只做旁观者。
- 这次重构把旧页里分散的定义改成一条完整教学链：
  1. 先分清三种资料集各自读什么、写什么。
  2. 再把 validation selection 写成一个更小的 `H_val` 上的选择问题。
  3. 然后用状态账本说明哪里会被污染、哪里会失效。
  4. 最后落到实验设计、代码读写和常见失败。
- 本页不扩展到 cross-validation、nested validation、Bayesian optimization 或 leaderboard 规则治理；这些留给后面的学习和别的场景。
- 任何具体操作建议都只基于当前课程页和课程顺序，不引入外部仓库或私有作业。
