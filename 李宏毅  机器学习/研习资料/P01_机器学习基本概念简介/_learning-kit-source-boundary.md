# P01_机器学习基本概念简介 本地来源说明

## Source Boundary

- 课程目录页：`../index.html`
  - 用来确认 P01 在整门课程中的位置，以及它和 P02、P03、P10 的衔接关系。
- 课程说明：`../README.md`
  - 用来确认整门课程的命名方式、完成状态和统一写法。
- 旧版 P01 学习页：`学习页.html`
  - 用来回收这一节已经出现过的核心概念、例子、代码桥和练习方向。

Snapshot: 本地文件于 2026-06-21 检查。

## Source-To-Unit Notes

- 这一节的核心，不是把机器学习讲成抽象口号，而是把它还原成一套可操作的语言：
  - 先说清输入和输出
  - 再把任务翻成函数
  - 再区分 model、parameter、hyperparameter、loss、optimization
  - 最后把训练资料和未见资料分开看
- 旧页已经给出了完整主线，重构时保留并压实：
  - 机器学习是在找函数
  - 输出形态决定任务更接近 regression、classification，还是 structured learning
  - model 是带未知参数的函数
  - loss 把“好不好”变成可以优化的数字
  - optimization 负责把参数往更好的方向推
  - training / validation / test 的角色不同，低 training loss 不等于真正学会
  - 最小线性回归代码可以把三步流程串起来
- 这次重构把碎片式讲解整理成一条连续教学链：
  1. 先把“机器学习”说成一个更精确的任务：低 loss、泛化和参数效率要一起看。
  2. 再把 universal approximation 和 `piecewise linear`、`ReLU` 接起来，先说明“能做到”。
  3. 然后说明为什么深层结构有机会更省参数，重点落在 `2k` / `2^k` 的对比。
  4. 接着用 parity、module、折纸/折叠把“中间表示复用”讲扎实。
  5. 再用 `tent` / `deep_fold` 代码和状态表把折叠过程手工走一遍。
  6. 最后补边界、误区和下一节衔接。
- 本页不扩展到 batch norm、残差网络、优化技巧、卷积架构细节、规模化训练或后续注意力机制的内部结构；这些留给别的单元展开。
- 任何具体操作建议都只基于当前课程页和课程顺序，不引入外部仓库、私有作业或未检查的结论。
