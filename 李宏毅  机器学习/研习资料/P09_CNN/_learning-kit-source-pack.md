# P09_CNN 本地 Source Pack

## Source Boundary

- 课程目录索引：`D:/Users/yyh/Downloads/笔记库/30_研究/李宏毅  机器学习/研习资料/index.html`
  - 用来确认 P09 在整门课中的位置，以及前后单元的承接关系。
- 现有旧页：`D:/Users/yyh/Downloads/笔记库/30_研究/李宏毅  机器学习/研习资料/P09_CNN/学习页.html`
  - 用来提取这节课已经覆盖的概念、例子、练习和代码桥。
- 课程说明：`D:/Users/yyh/Downloads/笔记库/30_研究/李宏毅  机器学习/研习资料/README.md`
  - 用来确认课程已覆盖到 P09 以及统一的课程命名风格。

Snapshot: local files inspected on 2026-06-20.

## Source-To-Unit Notes

- 课程 index 把 P09 排在 P08 之后、P10 之前，所以这节课的主任务是从“模型复杂度与泛化”过渡到“图像任务的结构归纳偏置”。
- 旧页的主线分成几块：
  - 图片是 `H×W×C` tensor，直接拉平成向量再接全连接层会让参数量暴涨。
  - `receptive field` 说明一个 neuron 只需要看局部区域。
  - `parameter sharing` 说明同一个 pattern detector 可以在不同位置复用。
  - 卷积会生成 `feature map`，多个 filter 会对应多个输出通道。
  - `pooling` 的作用是下采样、减小空间尺寸、降低运算量，但不是必须。
  - 旧页没有把卷积和 pooling 的输出尺寸公式单独展开；本次重构把 `stride`、`padding`、`floor` 和 `flatten` 的 shape 变化单独讲开，补上了这一块。
  - 典型流程是 `conv -> pool -> flatten -> fully connected`。
  - 适用边界要明确：CNN 对旋转、缩放并不天然不变，任务是否适合要重新检查。
- 旧页的代码桥是一个简化的 PyTorch CNN：
  - `Conv2d -> ReLU -> MaxPool2d -> Conv2d -> MaxPool2d -> flatten -> Linear`
  - 重点检查输入 channel、输出 channel、kernel size、padding、pooling 和 flatten 的作用。
- 旧页的练习主题集中在：
  - 图片参数量估算
  - receptive field / filter / feature map / pooling
  - AlphaGo 为什么能用 CNN、但不适合随便用 pooling
  - CNN 为什么不是“天然处理旋转和缩放”
  - 费曼式总结：为什么 CNN 适合图像

## Inferred Teaching Order

1. 先从图像输入和参数爆炸讲起。
2. 再讲局部连接和 receptive field。
3. 接着讲 parameter sharing、filter 和 feature map。
4. 然后讲 pooling 的价值和代价。
5. 再把这些概念收进一个典型 CNN 分类器流程里。
6. 最后讲适用边界、常见误区和 PyTorch 代码阅读。

## Gaps And Decisions

- 这一节不扩展到 batch norm、残差网络、目标检测、语义分割、现代 backbone 或频域解释。
- 不把 pooling 写成必需品，也不把 CNN 写成万能结构。
- 任何关于“更适合哪些任务”的判断，只能作为基于现有课程内容的教学建议，不当成新增事实。
