from __future__ import annotations

import json
import re
from pathlib import Path

from lxml import etree, html


ROOT = Path(r"D:\Users\yyh\Downloads\笔记库\30_研究\PyTorch深度学习实践 刘二大人\研习资料")
COURSE = "PyTorch 深度学习实践 刘二大人"
VENDOR_LINKS = [
    ("../assets/vendor/katex/katex.min.css", "stylesheet"),
    ("../assets/vendor/prism/prism-tomorrow.min.css", "stylesheet"),
    ("../assets/vendor/prism/prism-line-numbers.min.css", "stylesheet"),
    ("../assets/study-page.css", "stylesheet"),
]
VENDOR_SCRIPTS = [
    "../assets/vendor/katex/katex.min.js",
    "../assets/vendor/katex/auto-render.min.js",
    "../assets/vendor/prism/prism-core.min.js",
    "../assets/vendor/prism/prism-clike.min.js",
    "../assets/vendor/prism/prism-python.min.js",
    "../assets/vendor/prism/prism-bash.min.js",
    "../assets/vendor/prism/prism-json.min.js",
    "../assets/vendor/prism/prism-line-numbers.min.js",
    "../assets/study-page.js",
]

PAGE_CONFIG = {
    "09": {
        "path": ROOT / "09_多分类问题：Softmax、交叉熵与MNIST" / "学习页.html",
        "unit": "09 多分类问题：Softmax、交叉熵与 MNIST",
        "shape": [
            {"id": "logits", "label": "logits", "hint": "[B,10]", "title": "原始分数", "body": "每个样本先保留 10 个类别分数，不急着转概率。"},
            {"id": "softmax", "label": "softmax", "hint": "归一化", "title": "概率分布", "body": "把一行分数变成和为 1 的概率，方便解释。"},
            {"id": "labels", "label": "labels", "hint": "long [B]", "title": "类别索引", "body": "训练标签保持为类别编号，不必改成 one-hot。"},
            {"id": "loss", "label": "CrossEntropy", "hint": "标量", "title": "损失值", "body": "训练时直接把 logits 和 long 标签送进损失函数。"},
            {"id": "pred", "label": "argmax", "hint": "类别", "title": "预测结果", "body": "评估时再取最大分数的位置，得到最终类别。"},
        ],
        "detail": "围绕当前题目给出特定反馈：点明 logits、softmax、CrossEntropyLoss、类别索引或 argmax 中真正相关的一环，并写清 shape 或 dtype 依据。",
        "answers": {
            "q1": "10",
            "q2": "错误：CrossEntropyLoss 默认接收 logits，不要先手动 softmax",
            "q3": "784",
        },
        "explain": {
            "q1": "每个类别一个分数。",
            "q2": "训练时直接喂 logits。",
            "q3": "1×28×28=784。",
        },
        "formula": "Softmax 与 CrossEntropy 公式",
        "trace": "多分类追踪表",
        "worked_title": "完整样例：一批 MNIST logits 的读法",
        "worked_intro": [
            "拿一批 shape 是 [B, 1, 28, 28] 的灰度图时，第一件事不是想 softmax，而是先把输入和标签放到同一条账本上。模型前向会先把图像展平或交给卷积骨架，最后吐出 [B, 10] 的 logits。这里的 10 对应十个类别，每个位置都只是原始分数。",
            "训练时，`CrossEntropyLoss` 直接读取 logits 和 long 类型标签。它不需要 one-hot，也不需要你先把分数转成概率。真正该保留的是 shape、dtype 和类别索引这三样东西。只要这三样对齐，训练闭环就能跑通。",
            "评估时再看 softmax 和 argmax：softmax 用来解释概率，argmax 用来取预测类别。把这两件事和训练损失分开，你才不会把“展示用的概率”误当成“训练用的输入”。",
            "如果你看到 loss 在下降但准确率不动，优先回到这条账本：logits 的最后一维是不是 10，标签是不是 long，是否把 softmax 先做在前面。多数多分类错题都不是数学推导错误，而是接口顺序写反了。",
        ],
        "worked_table": [
            ("输入", "[B, 1, 28, 28]", "灰度批次", "先确认 batch 和空间维"),
            ("展平后", "[B, 784]", "进入全连接骨架", "只有这里适合 Linear"),
            ("输出", "[B, 10]", "十类 logits", "每行十个原始分数"),
            ("标签", "[B]", "long 类别索引", "CrossEntropyLoss 直接读取"),
        ],
        "worked_code": """import torch

images = torch.randn(4, 1, 28, 28)
labels = torch.tensor([7, 2, 1, 0], dtype=torch.long)
logits = model(images.view(images.size(0), -1))
loss = criterion(logits, labels)
pred = logits.argmax(dim=1)
print(logits.shape, loss.item(), pred.tolist())""",
        "bridge_title": "第二条教学链：从错误信号回头查接口",
        "bridge_paras": [
            "多分类最常见的坏味道，是代码能跑但结果不可信。你要先把故障分成三类：输出维度不够、标签 dtype 不对、训练前多做了一次 softmax。这个分类很重要，因为这三类问题对应的修法完全不同。输出维度不够，改模型最后一层；dtype 不对，改标签构造；softmax 放错位置，改 loss 前的输入。",
            "再往下查时，不要盯着 accuracy 的数字发呆。先打印 logits 的 shape，再打印 labels 的 dtype，最后看模型在 loss 前到底喂了什么。`CrossEntropyLoss` 想要的是未归一化分数和 long 标签，不是已经变成概率的张量。只要这句约定不记错，大多数多分类调试都能回到正轨。",
            "一旦模型从图像走到类别分数，你可以用一个小样本把完整路径复读一遍：输入是 `[B, 1, 28, 28]`，中间经过展平或卷积骨架，最后输出 `[B, 10]`。这一条链路上，只有最后一维和标签语义真的会影响 loss，前面那些中间层只是改变表示，不是改任务。换句话说，训练不稳时，优先怀疑接口顺序，而不是怀疑数学。"
        ],
        "bridge_table": [
            ("输出太小", "最后一层不是 10 维", "十分类任务却只给了一个分数", "把最后一层改成 num_classes"),
            ("标签太松", "标签是 float 或 one-hot", "默认 CrossEntropyLoss 不按这套读", "改成 long 类别索引"),
            ("概率太早", "先 softmax 再算 loss", "把训练输入和展示输入混了", "训练时直接传 logits"),
            ("验证太晚", "只看 loss 不看样本", "数值在变，语义未必对", "把 shape、dtype 和预测样本一起看"),
        ],
        "bridge_code": """logits = model(batch_x)
if logits.shape[-1] != 10:
    raise ValueError("expect 10 classes")
if batch_y.dtype != torch.long:
    batch_y = batch_y.long()
loss = criterion(logits, batch_y)
print("shape:", logits.shape, "loss:", float(loss))""",
        "appendix_title": "实现一致性：把训练、评估和记录对齐",
        "appendix_paras": [
            "多分类这一讲真正要练熟的，不只是会写 `CrossEntropyLoss`，而是会在训练前就把输入、输出、标签和评估指标放到同一页上。你可以把它理解成一个小账本：输入是图片，输出是十类分数，标签是类别索引，评估时再把分数转成可解释的概率。四者语义一致，训练才有意义。",
            "判断模型是否对齐，不一定要先跑完整个 epoch。更稳的办法，是拿一个小 batch 直接打印 shape 和 dtype：`logits.shape`、`labels.dtype`、`pred.shape`。只要这三项都像预期，后续的错误大多不是框架问题，而是数据管道或者损失调用顺序出了偏差。",
            "如果你想把这节课真的用起来，就别只盯着最终准确率。先看一条样本能不能从输入流到 logits，再看一个 batch 能不能得到稳定的 loss，最后再看预测类别是不是和直觉一致。这个顺序比“先跑再说”更省时间，也更容易定位 bug。",
            "另一个很实用的习惯，是把训练和评估写成两个固定模板。训练模板负责 `zero_grad -> backward -> step`，评估模板负责 `eval -> no_grad -> argmax -> 统计`。你只要不混用这两套模板，很多‘为什么结果忽高忽低’的问题会直接少一半。",
            "当你需要换任务，比如从 MNIST 换到别的十分类数据时，先别改学习率，先改接口：输入 shape、标签范围、最后一层输出维度、损失函数输入约定。只要这四项对齐，参数调节才有意义；如果它们没对齐，调得再久也只是修表象。",
            "你还可以给自己留一个极小的复盘模板：先写输入、输出和标签，再写 loss 的输入约定，最后看预测类别和真实标签是否对得上。这个模板很短，但每次都能帮你快速回到问题本身。真正有用的不是把流程背下来，而是把流程变成你会重复执行的检查动作。",
            "如果要从这一讲迁移到别的分类任务，最值得优先修改的永远不是优化器，而是输出维度和标签编码。只要这两项改对，后面的学习率、batch size 和训练轮数才有讨论意义。换句话说，先对齐接口，再谈训练细节。",
        ],
        "appendix_table": [
            ("训练前", "确认输入/标签/输出", "先看 shape 和 dtype", "直接避免接口误接"),
            ("训练中", "监控 loss", "看 loss 是否真的下降", "不是每个下降都代表学对"),
            ("验证时", "看 argmax 结果", "对照真实标签", "发现类别错位"),
            ("切任务", "改最后一层与标签", "num_classes 和标签范围", "换任务时最容易漏改"),
        ],
        "appendix_code": """batch_x = batch_x.float()
batch_y = batch_y.long()
logits = model(batch_x)
assert logits.shape[-1] == 10
loss = criterion(logits, batch_y)
with torch.no_grad():
    pred = logits.argmax(dim=1)
    acc = (pred == batch_y).float().mean()
print("loss:", float(loss), "acc:", float(acc))""",
    },
    "10": {
        "path": ROOT / "10_卷积神经网络基础：通道、卷积核与池化" / "学习页.html",
        "unit": "10 卷积神经网络基础：通道、卷积核与池化",
        "shape": [
            {"id": "input", "label": "NCHW", "hint": "输入", "title": "图像批次", "body": "先看 batch、通道和空间尺寸，别急着读分类头。"},
            {"id": "conv", "label": "conv", "hint": "提特征", "title": "卷积特征", "body": "卷积先改通道语义，再决定高宽怎么变化。"},
            {"id": "pool", "label": "pool", "hint": "下采样", "title": "池化结果", "body": "池化主要缩小高宽，保住更粗的空间信息。"},
            {"id": "flat", "label": "flatten", "hint": "展平", "title": "分类前向量", "body": "进入 Linear 之前要把最后的空间维摊平。"},
            {"id": "head", "label": "linear", "hint": "类别", "title": "分类 logits", "body": "最后一层只负责输出类别分数。"},
        ],
        "detail": "围绕当前题目给出特定反馈：先点明正确结论，再解释它在 NCHW、通道、高宽、展平或分类头链路中的位置。",
        "answers": {
            "q1": "[N,C,H,W]",
            "q2": "错误：MaxPool2d(2) 通常缩小高宽，不改变通道数",
            "q3": "3",
        },
        "explain": {
            "q1": "按 PyTorch 约定。",
            "q2": "池化主要缩小空间尺寸。",
            "q3": "RGB 常见是 3 个通道。",
        },
        "formula": "卷积与池化的尺寸变化",
        "trace": "CNN shape 追踪表",
        "worked_title": "完整样例：一张 28×28 图像怎么走到分类头",
        "worked_intro": [
            "卷积网络最容易乱的地方，不是卷积公式，而是 NCHW 和通道数。拿 `[32, 1, 28, 28]` 这一批图像来说，Conv2d 先读输入通道，再决定输出通道和空间尺寸。你看到的不是“图像变复杂了”，而是“特征图换了一种组织方式”。",
            "池化层的任务更窄：它主要缩小高宽，不负责改类别数。很多报错都来自把池化和卷积混成一类操作，结果把通道数和空间尺寸一起算错。真正该盯的是每一步后张量的 shape，而不是层名字本身。",
            "到了分类头，所有特征图都要先摊平。`view(x.size(0), -1)` 的意思不是“随便压扁”，而是保住 batch，把剩下的空间和通道合成一条特征轴。这样 `Linear` 才能继续读。",
            "如果把图像先展平再送进 Conv2d，空间结构会被抹掉；如果忘了改 `in_channels`，第二层卷积会直接读错输入。读 CNN 时，先把 shape 账本写对，再去看特征语义，顺序不能反。",
        ],
        "worked_table": [
            ("输入", "[32, 1, 28, 28]", "灰度图像批次", "先看通道是 1"),
            ("卷积后", "[32, 10, 24, 24]", "10 个特征图", "高宽缩小 4"),
            ("池化后", "[32, 10, 12, 12]", "更粗的空间信息", "通道不变"),
            ("展平后", "[32, 1440]", "Linear 输入", "把空间和通道折叠"),
        ],
        "worked_code": """import torch

x = torch.randn(32, 1, 28, 28)
x = conv1(x)
x = pool(x)
x = x.view(x.size(0), -1)
logits = head(x)
print(x.shape, logits.shape)""",
        "bridge_title": "第二条教学链：把 shape 账本记到分类头",
        "bridge_paras": [
            "CNN 的调试，第一步永远不是“卷积参数对不对”，而是“每一层后的 shape 有没有按预期变化”。只要输入是 `[N, C, H, W]`，那就先看 `C` 有没有被卷积层接住，再看 `H` 和 `W` 有没有被 kernel、stride、padding 改掉。高宽的变化能不能解释通，是判断网络结构是否接上的最快办法。",
            "很多人会把池化层当成“也能改通道”的东西，这会把整条链路直接算歪。池化的职责很窄，它只负责压缩空间维；卷积才是把通道从 1 变成 10、从 10 变成 20 的地方。等你把这两个动作拆开，再去读 `conv -> relu -> pool -> flatten -> linear`，每一步就都有明确目的，不会再看成机械堆层。",
            "对于分类头来说，`view(x.size(0), -1)` 不是可有可无的写法，而是把空间轴交给 Linear 的那一步。你可以把它理解成“把一块特征图整理成一条特征向量”。如果这一步做错，后面的线性层就会拿错输入，错误信息常常表现为维度不匹配，而不是语义报错。",
            "在真正的图像任务里，你最好养成一个小习惯：每一个 block 后都打印一次 shape，至少在第一次实现时这样做。先确认通道和空间尺寸，再确认分类头，再看 loss。这个顺序能避免最常见的误判，也能让你读陌生 CNN 时更快分辨哪些地方是在提特征，哪些地方只是在降尺寸。"
        ],
        "bridge_table": [
            ("卷积前", "[N, 1, 28, 28]", "原始图像", "先看通道是否接对"),
            ("卷积后", "[N, 10, 24, 24]", "特征图变厚", "通道和空间同时改变"),
            ("池化后", "[N, 10, 12, 12]", "更粗的格局", "只压缩高宽"),
            ("展平后", "[N, 1440]", "喂给 Linear", "把卷积输出整理成向量"),
        ],
        "bridge_code": """def forward(self, x):
    print("input:", x.shape)
    x = self.conv1(x)
    print("after conv1:", x.shape)
    x = self.pool(x)
    print("after pool:", x.shape)
    x = x.view(x.size(0), -1)
    return self.fc(x)""",
        "appendix_title": "实现一致性：把 CNN 的每一步写成检查表",
        "appendix_paras": [
            "卷积网络最值得练习的，不是背卷积公式，而是把每一步的张量形状写明白。你拿到输入以后，先记住它是 `[N, C, H, W]`，然后沿着卷积、池化、展平、Linear 的顺序去看。只要这条顺序不乱，CNN 的代码通常就很好读。",
            "调试 CNN 时，最有效的动作往往不是修改网络，而是打印中间 shape。你要知道 Conv2d 改的是通道和空间，MaxPool2d 主要改空间，Linear 才看最后的特征轴。如果这三类动作被你混成一类，报错信息会很像，但修法完全不同。",
            "很多人第一次写 CNN，会在分类头前面漏掉展平。这个错误的本质不是“忘记一行代码”，而是忘了把卷积输出整理成向量。把特征图摊平这一动作看成一个接口转换，你就会更容易理解为什么 `view(x.size(0), -1)` 这行不能省。",
            "还有一个容易漏掉的点，是不同卷积层的通道必须接上。第一层输出 10 个通道，第二层就要读 10 个通道；如果第二层还写成 1，模型就像把上一层的结果当成另一种数据看。这个错经常在报错中直接体现为通道数不匹配。",
            "做题时你可以按三个层次回答：先说 shape 怎么变，再说每一步的职责，最后说哪里最容易错。这样写出来的答案比只写一句‘卷积提特征、池化降尺寸’更能拿来真正调试。",
            "如果你想把 CNN 的知识真的用起来，最好每次先在纸上写一遍 `NCHW -> Conv -> Pool -> Flatten -> Linear`。这个小动作能把很多模糊的直觉变成可检查的顺序，也会让你在读开源代码时更快找到 block 的边界。",
            "卷积并不是单纯把图像变小，它更像是在一条固定格式的张量账本上，连续改写通道和空间尺寸。你只要把每一步写成‘输入 shape -> 输出 shape -> 负责什么’，就会发现很多看似复杂的 CNN 其实只是同一种模式重复。",
            "如果训练结果一直怪，先回到最前面看输入是不是灰度还是 RGB，通道数有没有对上，最后一层是不是和类别数一致。这个从头到尾的检查，比在中间层里盲目试错更靠谱。"
        ],
        "appendix_table": [
            ("输入", "[N, C, H, W]", "先看通道", "别把 batch 和通道混了"),
            ("卷积", "改通道 / 高宽", "核大小和 stride", "输出 shape 要算清"),
            ("池化", "压缩高宽", "下采样", "不负责改变类别数"),
            ("Linear", "最后一维", "分类前向量", "忘记展平就会卡住"),
        ],
        "appendix_code": """x = torch.randn(16, 1, 28, 28)
print("start", x.shape)
x = self.conv1(x)
print("conv1", x.shape)
x = self.pool(x)
print("pool", x.shape)
x = x.view(x.size(0), -1)
logits = self.fc(x)
print("logits", logits.shape)""",
    },
    "11": {
        "path": ROOT / "11_卷积神经网络高级篇：Inception、残差与读代码" / "学习页.html",
        "unit": "11 卷积神经网络高级篇：Inception、残差与读代码",
        "shape": [
            {"id": "branches", "label": "branches", "hint": "多分支", "title": "并行分支", "body": "先分支、再汇合，读代码时先看每支输出什么。"},
            {"id": "concat", "label": "cat(dim=1)", "hint": "拼通道", "title": "通道拼接", "body": "Inception 这类结构常沿通道维拼起来。"},
            {"id": "skip", "label": "shortcut", "hint": "残差", "title": "跳连相加", "body": "Residual 不是拼接，而是逐元素相加。"},
            {"id": "align", "label": "1x1 conv", "hint": "对齐", "title": "通道对齐", "body": "1x1 卷积常用来改通道数，方便相加或降计算量。"},
            {"id": "head", "label": "head", "hint": "输出", "title": "分类头", "body": "最后还是回到 logits，训练接口不需要换。"},
        ],
        "detail": "围绕当前题目给出特定反馈：区分多分支拼接、残差相加或 1x1 卷积中的具体规则，并说明对应 shape 约束。",
        "answers": {
            "q1": "通道维 dim=1",
            "q2": "错误：残差相加前 shape 必须能逐元素对齐",
            "q3": "通道",
        },
        "explain": {
            "q1": "NCHW 下拼接通常走通道维。",
            "q2": "相加前必须 shape 对齐。",
            "q3": "1x1 卷积常改通道数。",
        },
        "formula": "Inception 与残差的接口",
        "trace": "多分支追踪表",
        "worked_title": "完整样例：Inception 和残差在一条账本里怎么读",
        "worked_intro": [
            "Inception 的关键不是“层很多”，而是“分支很多”。同一个输入会进入不同卷积核或不同尺度的路径，最后沿通道维拼在一起。只要分支在高宽上对齐，`torch.cat(..., dim=1)` 就能把它们接成一个更厚的特征图。",
            "Residual 的关键也不是“加法”，而是“相加前要先对齐”。`shortcut` 这条线把输入直接送到后面，和主分支逐元素相加。两边 shape 对不上时，`1x1` 卷积经常被拿来调通道和步幅。",
            "读这类代码时，要先问自己：每个分支读什么、写什么、最后是拼接还是相加。把这个问题答清楚，后面的 `forward` 就不再像一串抽象 API，而是几条并行的数据流。",
            "一旦你把 `cat` 和 `+` 分开，调试也就有了起点。拼接错多半是空间尺寸不一致；相加错多半是通道或步幅不一致。先把错归类，再看具体参数，修复会快很多。",
        ],
        "worked_table": [
            ("分支 A", "[B,16,H,W]", "局部特征", "和其他分支拼通道"),
            ("分支 B", "[B,24,H,W]", "更大感受野", "保持高宽一致"),
            ("拼接", "[B,40,H,W]", "沿 dim=1 合并", "通道相加不是相加数值"),
            ("残差", "[B,C,H,W]", "逐元素相加", "两边 shape 必须一致"),
        ],
        "worked_code": """import torch

y1 = branch1(x)
y2 = branch2(x)
y3 = branch3(x)
merged = torch.cat([y1, y2, y3], dim=1)
out = merged + shortcut
print(merged.shape, out.shape)""",
        "bridge_title": "第二条教学链：先分支，再汇合，再对齐",
        "bridge_paras": [
            "高级 CNN 读起来比基础 CNN 更绕，原因不在公式，而在“流向变多了”。Inception 把同一个输入切成多条路，每条路读到的东西不同，但最后一定要在高宽上对齐后再拼接。你看到的不是多个模型，而是一个模型里的多种感受野。",
            "残差块更容易误解。它不是“再来一次相加”这么简单，而是把原始输入保留下来，和主分支的结果做逐元素相加。只要这两边 shape 不一致，程序就会报错。于是你会发现，高级结构的调试顺序和基础结构一样，还是先看 shape，再看语义。",
            "对读代码的人来说，最有用的习惯不是记住某个块的名字，而是把每个分支的输入、输出和连接方式写出来。`cat` 代表拼接，`+` 代表相加，`1x1` 卷积经常是对齐工具。只要这三个概念被你分清，Inception 和 ResNet 的源码就会比注释更直白。",
            "这页的价值不只是认识两个经典模块，而是学会一条通用的追踪方法：先把多分支输出写成表，再检查哪里是通道拼接、哪里是逐元素相加，最后把它们放回主干网络。这样你读更复杂的网络时，不会被结构名字带偏，而是直接抓数据流。"
        ],
        "bridge_table": [
            ("并行分支", "[B,C,H,W]", "不同卷积核", "读每支自己的输出"),
            ("通道拼接", "[B,C1+C2,H,W]", "merge 通道", "只沿 dim=1 合并"),
            ("残差相加", "[B,C,H,W]", "逐元素相加", "两边 shape 必须一致"),
            ("1x1 conv", "[B,C',H,W]", "调整通道", "对齐 shortcut 或压计算量"),
        ],
        "bridge_code": """branch_a = conv1(x)
branch_b = conv3(x)
branch_c = pool(x)
merged = torch.cat([branch_a, branch_b, branch_c], dim=1)
if merged.shape != shortcut.shape:
    shortcut = adjust(shortcut)
out = merged + shortcut""",
        "appendix_title": "实现一致性：把多分支读成一张流程图",
        "appendix_paras": [
            "Inception 和 ResNet 这类块，最怕你把结构名记住了，却没把数据流记住。多分支结构里，输入会被复制到不同路径；残差结构里，原输入还会保留一条 shortcut。读源码时，如果你不能说清楚每条路读什么、写什么，后面就很容易在拼接和相加之间弄混。",
            "一个实用的判断方法，是先看输出是拼接还是相加。拼接一般意味着通道维变厚，但高宽不变；相加一般意味着 shape 要完全对齐。于是你能反推出，拼接类模块在设计时更关注多尺度特征，而残差类模块更关注信息直通和梯度路径。",
            "当你在调试高级 CNN 时，最常见的不是数学错，而是分支对齐错。某个分支少了 padding，另一个分支 stride 不一样，最后拼接或相加就炸了。别急着换块，先把每个分支的输入输出打印出来，再检查哪里没对齐。",
            "如果你愿意把每个 block 都写成一张表，读代码的速度会快很多。表里只要有输入、输出、连接方式、常见错误这四项，绝大多数卷积结构都能被你拆开。结构再复杂，也只是这几种动作的重复和组合。",
            "这也是为什么高级 CNN 依旧能用普通 CrossEntropy 训练：无论内部怎么分支、怎么跳连，最后都还是输出 logits。只要这个输出形状和任务类别数一致，损失函数就不需要为了结构复杂而改变。",
            "在看开源模型时，最好先定位 `forward` 的入口和出口，再回头看中间每个分支。你不用一开始就理解所有模块，只要先知道哪条路是主干、哪条路是旁路、最后在哪里合并，后面每个层的作用就会自然清楚。",
            "当你把这类结构读顺之后，再回去看 plain CNN，你会发现它其实就是多分支网络的简化版：少了旁路，少了拼接，但 shape 账本仍然是同一套。这个认识能让你在不同结构之间迁移得更快。",
            "你还可以给高级 CNN 准备一份专属检查表：分支输入是否一致、分支输出是否同高宽、拼接后通道数有没有变厚、残差相加前有没有对齐。把这四步写在纸上，读任何 Inception 或 ResNet 代码都会更稳。",
            "如果某个结构看着很复杂，先把它简化成‘并行计算 + 合并’这两个动作，再看它是拼接还是相加。这样你不会被模块名字吓住，而是会直接把注意力放到张量流向上。"
        ],
        "appendix_table": [
            ("分支输入", "[B,C,H,W]", "复制同一份张量", "注意每支自己的卷积参数"),
            ("拼接输出", "[B,C',H,W]", "沿通道合并", "高宽必须先对齐"),
            ("残差输出", "[B,C,H,W]", "逐元素相加", "shape 要完全相同"),
            ("1x1 对齐", "[B,C'',H,W]", "调整通道或步幅", "shortcut 常用它补接口"),
        ],
        "appendix_code": """y1 = self.branch1(x)
y2 = self.branch2(x)
y3 = self.branch3(x)
merged = torch.cat([y1, y2, y3], dim=1)
if merged.shape != x.shape:
    x = self.shortcut(x)
out = merged + x
print(merged.shape, out.shape)""",
    },
    "12": {
        "path": ROOT / "12_循环神经网络基础：序列、隐藏状态与RNNCell" / "学习页.html",
        "unit": "12 循环神经网络基础：序列、隐藏状态与RNNCell",
        "shape": [
            {"id": "seq", "label": "sequence", "hint": "输入", "title": "序列批次", "body": "先看 batch、时间步和特征维，再看 hidden。"},
            {"id": "hidden", "label": "hidden", "hint": "记忆", "title": "隐藏状态", "body": "hidden 只保存已经读过的序列信息。"},
            {"id": "cell", "label": "RNNCell", "hint": "一步", "title": "单步更新", "body": "RNNCell 只处理一个时间步，外面要自己写循环。"},
            {"id": "loop", "label": "loop", "hint": "展开", "title": "时间循环", "body": "整段序列就是沿时间步不断更新 hidden。"},
            {"id": "head", "label": "linear", "hint": "分类", "title": "序列分类头", "body": "最后一个 hidden 常接线性层，输出类别 logits。"},
        ],
        "detail": "围绕当前题目给出特定反馈：说明 sequence、hidden、batch_first、RNNCell/RNN 或时间步循环中真正相关的约束。",
        "answers": {
            "q1": "已经读过的序列信息",
            "q2": "错误：RNNCell 只处理一个时间步，完整序列需要循环",
            "q3": "seq_len",
        },
        "explain": {
            "q1": "hidden 里装的是已读过的上下文。",
            "q2": "Cell 只是一小步，不会自动扫完整段序列。",
            "q3": "batch_first 后时间步在中间那一维。",
        },
        "formula": "RNN 时间步更新",
        "trace": "RNN 时间步追踪表",
        "worked_title": "完整样例：RNN 一步一步读序列",
        "worked_intro": [
            "RNN 最容易弄混的就是时间步和 batch。`batch_first=True` 时，输入形状通常写成 `[B, S, F]`，其中 `B` 是样本数，`S` 是时间步数，`F` 是每步的特征数。只要这三个符号不乱，RNN 代码就好读很多。",
            "`nn.RNNCell` 只负责一小步：它读当前 `x_t` 和上一步 `h_{t-1}`，吐出新的 `h_t`。如果想读完整个序列，就要把它放进一个 for 循环。这个循环不是装饰品，而是模型真正“沿时间展开”的地方。",
            "序列分类通常只取最后一个 hidden 送进线性层。这个 hidden 里已经压进了前面所有时间步的信息，所以它更像摘要，而不是最终类别。真正的类别预测，还是要靠后面的分类头。",
            "如果你把 `[B, S, F]` 和 `[S, B, F]` 互换了，RNN 会把 batch 和时间步读反，后续 hidden 形状、loss 对齐和评估逻辑都会跟着乱掉。先定约定，再写代码，是这讲最值钱的习惯。",
        ],
        "worked_table": [
            ("输入序列", "[B,S,F]", "每步向量", "先分清 batch 和 seq"),
            ("单步 hidden", "[B,H]", "当前记忆", "来自上一时间步"),
            ("循环输出", "T 次更新", "逐步累计", "Cell 不会自己展开"),
            ("分类头", "[B,C]", "类别 logits", "最后一个 hidden 接 Linear"),
        ],
        "worked_code": """import torch

hidden = torch.zeros(batch_size, hidden_size)
for t in range(seq_len):
    x_t = sequence[:, t, :]
    hidden = cell(x_t, hidden)
logits = head(hidden)
print(hidden.shape, logits.shape)""",
        "bridge_title": "第二条教学链：把时间步和 batch 一起看",
        "bridge_paras": [
            "RNN 类题最容易错的地方，是你以为自己在看序列，实际上代码在看 batch。只要把 `[B, S, F]` 和 `[S, B, F]` 搞反，后面的 hidden、loss 和评估就会全部错位。学会在写代码前先选定一种输入约定，比记住任何一个 API 细节都重要。",
            "`RNNCell` 和 `RNN` 的区别，可以用一句话说明白：前者只处理一个时间步，后者帮你把整段序列展开。这个区别会直接影响你有没有写循环。你如果只调用一次 Cell，等于只读了一个 token；你如果让 RNN 接整段序列，才是在读上下文。",
            "序列分类和序列标注也要分开看。序列分类只需要最后一个 hidden；标注任务要每个时间步都出结果。两类任务的损失函数、输出 shape 和训练循环都不同。如果不先分任务，后面所有“为什么维度不对”的问题都会变成一团。",
            "因此，这页最值得带走的不是一个类名，而是一张时序账本：输入读哪一维、时间步怎么滚动、hidden 怎样传递、最后取哪一步做分类。把这张账本写出来，你再看任何 RNN 代码，都能知道是哪一层在读什么、哪一层在改什么。"
        ],
        "bridge_table": [
            ("输入", "[B,S,F]", "序列批次", "先分清 batch 和时间步"),
            ("Cell 更新", "[B,H]", "一步状态", "只读当前 x_t 和上一步 hidden"),
            ("整段 RNN", "[S,B,H] 或 [B,S,H]", "所有时间步", "要先定 batch_first"),
            ("分类头", "[B,C]", "类别 logits", "只取最后 hidden 时常见"),
        ],
        "bridge_code": """hidden = torch.zeros(batch_size, hidden_size)
for t in range(seq_len):
    x_t = sequence[:, t, :]
    hidden = cell(x_t, hidden)
if sequence.dim() != 3:
    raise ValueError("expect [B, S, F]")
logits = head(hidden)""",
        "appendix_title": "实现一致性：时间步、隐藏状态和输出头",
        "appendix_paras": [
            "RNN 的好处在于，它把‘顺序’这件事变成了显式的时间步更新。你只要把输入写成 `[B, S, F]`，后面每一轮循环都只做一件事：把当前 token 和上一步 hidden 合起来，得到下一步 hidden。这个过程非常机械，但正因为机械，才特别适合拿来排查 shape。",
            "很多人看到 `hidden` 会下意识把它当成最终分类结果，这是不对的。hidden 只是压缩后的中间状态，真正的类别还要经过线性层。这个区分很重要，因为你一旦把摘要和答案混起来，训练和推理的接口就会一起乱。",
            "RNNCell 和 RNN 的区别，也可以用调试视角理解。Cell 适合你想手动看每个时间步发生了什么；RNN 适合你已经确定输入约定，想直接让框架帮你展开。如果你读不懂某个序列模型，先把它拆回 Cell + for 循环，往往就能看清楚。",
            "在序列分类里，最后一个 hidden 常常最有用，因为它已经把前面所有时间步的信息压缩过了。可是一旦任务变成序列标注，你就不能只看最后一步，而要看每个时间步的输出。任务一换，输出头和损失函数就会跟着换。",
            "最容易出错的地方，还是 batch_first。你要么统一使用 `[B, S, F]`，要么统一使用 `[S, B, F]`，不要在一页里来回换。只要输入约定统一，hidden 的 batch 维也就自然能对齐。",
            "如果你想真正掌握这一讲，最好自己写一次手动循环，再写一次 `nn.RNN` 的版本，比较两者的输入和输出。这样你会发现，所谓‘神经网络的循环’，其实就是同一条状态链被重复调用多次。",
            "你还可以给序列模型准备一个简化版检查表：时间步是不是按顺序更新、hidden 的 shape 有没有变、最后的分类头是不是只读最后一步。这个表特别适合在你第一次写 `for t in range(seq_len)` 的时候用。"
        ],
        "appendix_table": [
            ("输入", "[B,S,F]", "时间步在中间", "batch_first 要统一"),
            ("Cell", "单步更新", "x_t + hidden", "只读一个时间点"),
            ("RNN", "整段展开", "返回序列摘要", "别把它和 Cell 混了"),
            ("输出头", "[B,C]", "类别 logits", "最后 hidden 再接 Linear"),
        ],
        "appendix_code": """hidden = torch.zeros(batch_size, hidden_size)
outputs = []
for t in range(seq_len):
    x_t = sequence[:, t, :]
    hidden = cell(x_t, hidden)
    outputs.append(hidden)
stacked = torch.stack(outputs, dim=1)
logits = head(stacked[:, -1, :])""",
    },
    "13": {
        "path": ROOT / "13_循环神经网络高级篇：Embedding、GRU与变长序列分类" / "学习页.html",
        "unit": "13 循环神经网络高级篇：Embedding、GRU 与变长序列分类",
        "shape": [
            {"id": "ids", "label": "ids", "hint": "索引", "title": "字符 id", "body": "先把字符串编码成 long 型索引，再送进 Embedding。"},
            {"id": "embed", "label": "Embedding", "hint": "查表", "title": "稠密向量", "body": "Embedding 把 id 变成可学习的向量表示。"},
            {"id": "lengths", "label": "lengths", "hint": "变长", "title": "真实长度", "body": "padding 只是补齐，真正有效的是每条序列的长度。"},
            {"id": "gru", "label": "GRU", "hint": "编码", "title": "序列编码", "body": "GRU 负责读序列依赖，最好配合 lengths 或 packing。"},
            {"id": "head", "label": "linear", "hint": "分类", "title": "分类 logits", "body": "最后还是把编码结果压成类别分数。"},
        ],
        "detail": "围绕当前题目给出特定反馈：说明 ids、Embedding、GRU、lengths、padding/packing、分类头或词表复用中真正相关的检查点。",
        "answers": {
            "q1": "long 类型的整数 id",
            "q2": "错误：pad 只是补齐占位，通常要避免当真实字符学习",
            "q3": "2",
        },
        "explain": {
            "q1": "Embedding 需要离散索引。",
            "q2": "pad 只负责占位，不该当成真实字符。",
            "q3": "双向 GRU 的方向数是 2。",
        },
        "formula": "Embedding 与 GRU 的接口",
        "trace": "变长序列追踪表",
        "worked_title": "完整样例：Embedding + GRU + packing 怎么连起来",
        "worked_intro": [
            "这一讲的名字分类器，第一步不是 GRU，而是编码。字符先变成 long 型 id，再经过 Embedding 查表，得到稠密向量。这里的关键是：输入已经不是字符串，而是可以被模型读的索引张量。",
            "名字长度不一，所以 batch 里通常要 padding 到同一长度。padding 只是为了堆叠成矩形，不是为了让模型学习这个占位符。真正该传给 RNN 的，是每条序列的真实长度，这样模型才知道哪些位置要忽略。",
            "GRU 读完以后，最后一个 hidden 通常作为分类摘要。若设置双向，最后的 hidden 还要考虑方向数，线性层输入维度往往要乘 2。这里的 shape 变化是最常见的调试点。",
            "如果词表在训练和推理时不一致，同一个字符可能落到不同 id 上，Embedding 查表的语义就会漂移。这个错误看起来像模型不稳定，实际上是编码规则改了。保存并复用同一套词表，比再调一次参数更重要。",
        ],
        "worked_table": [
            ("字符 id", "[B,S]", "long 索引", "先数字化再查表"),
            ("Embedding", "[B,S,E]", "稠密向量", "把离散符号变成可学习表示"),
            ("GRU", "[B,S,H]", "序列编码", "读完整个序列依赖"),
            ("分类头", "[B,C]", "类别 logits", "最后 hidden 接 Linear"),
        ],
        "worked_code": """import torch

ids = encode(names)
emb = embedding(ids)
packed = nn.utils.rnn.pack_padded_sequence(
    emb, lengths.cpu(), batch_first=True, enforce_sorted=False
)
_, hidden = gru(packed)
logits = fc(hidden[-1])
print(emb.shape, hidden.shape, logits.shape)""",
        "bridge_title": "第二条教学链：词表、长度和方向数一起查",
        "bridge_paras": [
            "Embedding、GRU 和变长序列最容易让人感觉“都懂了”，一到代码就对不上。其实你只需要按顺序检查四件事：字符是否先被编码成 id，id 是否是 long，padding 后有没有记录真实长度，GRU 的方向数是否影响了最后 hidden 的维度。只要这四件事逐个过关，绝大多数报错就能定位。",
            "变长序列的核心，不是把短序列补齐这么简单，而是让模型知道哪些位置只是占位。padding 只解决 batch 对齐，packing 才是让 RNN 少看无效 token。这个区别很工程，但它直接决定模型会不会把补零当成有效内容。",
            "名字分类这种任务特别适合拿来练“从编码到分类头”的整条链路。你先把字符转 id，再查 embedding，再让 GRU 读序列，最后取最后 hidden 做分类。每一步的对象都不同，职责也不同；只要你能把职责讲清楚，代码就不会只剩下形状检查。",
            "这一页最重要的收束点，是词表一定要复用。训练和推理如果用不同的字符表，同一个名字就会被编码成不同的 id，embedding 的意义会漂。这个问题表面上像是模型泛化差，实际上是输入语义变了。所以真正的工程检查，不只检查层，也要检查编码约定。"
        ],
        "bridge_table": [
            ("字符", "raw string", "先编码", "不能直接进 Embedding"),
            ("Embedding", "[B,S,E]", "稠密向量", "把 id 映射成可学表示"),
            ("GRU", "[B,S,H] / hidden", "序列编码", "读 sequence 依赖"),
            ("分类头", "[B,C]", "类别 logits", "最后 hidden 接 Linear"),
        ],
        "bridge_code": """ids = encode(names)
emb = embedding(ids)
packed = nn.utils.rnn.pack_padded_sequence(
    emb, lengths.cpu(), batch_first=True, enforce_sorted=False
)
_, hidden = gru(packed)
if hidden.size(0) == 2:
    hidden = hidden.sum(dim=0)
logits = fc(hidden[-1])""",
        "appendix_title": "实现一致性：编码、长度和词表一起校对",
        "appendix_paras": [
            "Embedding + GRU 这一讲，最值得固定下来的不是某个层名，而是编码顺序。先把字符转成 id，再查表成向量，再让 GRU 读序列，最后把 hidden 交给分类头。这个顺序一旦写对，后面的排错就很简单；写反了，整个模型都会像在读另一种语言。",
            "长度信息是这类任务的第二个关键点。padding 负责补齐 batch，lengths 负责告诉模型哪些位置是假的。只做 padding 不做 lengths，你会让 RNN 把补零当成真实字符，训练结果可能看起来能收敛，但语义已经偏了。",
            "双向 GRU 是第三个关键点。双向会把正向和反向的信息都读进来，所以最后 hidden 的方向数会变多，分类头输入维度常常要跟着翻倍。这个地方如果忘了改，报错一般很明确，但如果你只看模型结构名字，反而不容易第一时间想到它。",
            "真正落地时，词表复用比你想的更重要。训练和推理如果不是同一套映射，同一个字符可能在两个阶段变成不同 id，Embedding 的含义就变了。那种‘模型时好时坏’的现象，很多并不是模型本身的问题，而是输入编码漂移。",
            "所以这页的检查顺序应该是：字符是否编码、id 是否 long、padding 是否和 lengths 一起出现、GRU 的方向数是否影响分类头、最后有没有复用词表。把这一串检查养成习惯，你会少掉很多看似神秘的 bug。",
            "如果你把这一页的知识真的用到项目里，可以先做一个最小实验：只用三四个样本，把编码、padding、GRU 和分类头全部串起来。这个最小实验虽然简单，却能把编码层和模型层之间的接口问题先暴露出来。",
            "另外，双向 GRU 的 hidden 取法也值得专门记一下。很多时候你不是取一个向量就结束，而是要先把方向信息合并，再送进分类头。这个合并方式一变，分类层输入维度就要跟着动。"
        ],
        "appendix_table": [
            ("字符输入", "raw string", "先编码", "不能直接进 Embedding"),
            ("Embedding", "[B,S,E]", "向量表示", "查表后才可训练"),
            ("GRU", "[B,S,H]", "序列依赖", "方向数可能翻倍"),
            ("分类头", "[B,C]", "类别 logits", "最后 hidden 再接 Linear"),
        ],
        "appendix_code": """ids = encode(names)
assert ids.dtype == torch.long
emb = embedding(ids)
packed = nn.utils.rnn.pack_padded_sequence(
    emb, lengths.cpu(), batch_first=True, enforce_sorted=False
)
_, hidden = gru(packed)
if hidden.dim() == 3:
    hidden = hidden[-1]
logits = fc(hidden)""",
    },
}


def is_element(node: object) -> bool:
    return isinstance(node, etree._Element)


def add_class(node: etree._Element, class_name: str) -> None:
    classes = set((node.get("class") or "").split())
    classes.add(class_name)
    node.set("class", " ".join(sorted(classes, key=lambda item: item)))


def ensure_class(node: etree._Element, class_name: str) -> None:
    classes = (node.get("class") or "").split()
    if class_name not in classes:
        classes.append(class_name)
        node.set("class", " ".join(classes))


def set_text(node: etree._Element, text: str) -> None:
    node.clear()
    node.text = text


def append_child(parent: etree._Element, tag: str, attrib: dict[str, str] | None = None, text: str | None = None) -> etree._Element:
    child = etree.Element(tag, attrib=attrib or {})
    if text is not None:
        child.text = text
    parent.append(child)
    return child


def insert_after(ref: etree._Element, node: etree._Element) -> None:
    ref.addnext(node)


def insert_before(ref: etree._Element, node: etree._Element) -> None:
    ref.addprevious(node)


def first_text(node: etree._Element, xpath: str) -> str:
    found = node.xpath(xpath)
    if not found:
        return ""
    if isinstance(found[0], etree._ElementUnicodeResult):
        return str(found[0]).strip()
    if is_element(found[0]):
        return (found[0].text_content() or "").strip()
    return str(found[0]).strip()


def find_direct_next_element(node: etree._Element, tag: str) -> etree._Element | None:
    sib = node.getnext()
    while sib is not None:
        if is_element(sib) and sib.tag == tag:
            return sib
        if is_element(sib) and sib.tag in {"div", "section", "table", "pre", "script", "style"}:
            if sib.tag == tag:
                return sib
        sib = sib.getnext()
    return None


def make_shape_tracer(items: list[dict[str, str]]) -> etree._Element:
    root = etree.Element("div", attrib={"class": "shape-tracer", "data-shape-tracer": ""})
    lines = etree.SubElement(root, "div", attrib={"class": "trace-lines"})
    canvas = etree.SubElement(root, "div", attrib={"class": "trace-canvas"})
    for idx, item in enumerate(items):
        active = idx == 0
        line = etree.SubElement(
            lines,
            "button",
            attrib={
                "class": "trace-line active" if active else "trace-line",
                "type": "button",
                "data-trace-step": item["id"],
            },
        )
        code = etree.SubElement(line, "code")
        code.text = item["label"]
        span = etree.SubElement(line, "span")
        span.text = item["hint"]

        card = etree.SubElement(
            canvas,
            "div",
            attrib={
                "class": "tensor-card active" if active else "tensor-card",
                "data-trace-target": item["id"],
            },
        )
        title = etree.SubElement(card, "b")
        title.text = item["title"]
        short = etree.SubElement(card, "span")
        short.text = item["hint"]
        body = etree.SubElement(card, "p")
        body.text = item["body"]
    return root


def make_reveal_details(note: str) -> tuple[etree._Element, etree._Element]:
    button = etree.Element("button", attrib={"class": "reveal", "type": "button"})
    button.text = "展开反馈"
    details = etree.Element("details")
    summary = etree.SubElement(details, "summary")
    summary.text = "参考回答"
    para = etree.SubElement(details, "p")
    para.text = note
    return button, details


def style_block() -> etree._Element:
    raise NotImplementedError


def add_assets(head: etree._Element) -> None:
    for href, rel in VENDOR_LINKS:
        if not head.xpath(f'.//link[@href="{href}"]'):
            head.append(etree.Element("link", attrib={"rel": rel, "href": href}))


def add_scripts(body: etree._Element) -> None:
    for src in VENDOR_SCRIPTS:
        if not body.xpath(f'.//script[@src="{src}"]'):
            body.append(etree.Element("script", attrib={"src": src}))


def clean_inline_assets(root: etree._Element) -> None:
    for style in root.xpath(".//style"):
        parent = style.getparent()
        if parent is not None:
            parent.remove(style)
    for script in root.xpath(".//script[not(@src)]"):
        parent = script.getparent()
        if parent is not None:
            parent.remove(script)


def update_head_body(root: etree._Element, cfg: dict[str, object]) -> None:
    head = root.xpath("/html/head")[0]
    body = root.xpath("/html/body")[0]
    body.set("data-course", COURSE)
    body.set("data-unit", str(cfg["unit"]))
    brand = body.xpath('.//div[@class="brand"]')
    if brand:
        brand_block = brand[0]
        strong = brand_block.xpath(".//strong")
    if strong:
        set_text(strong[0], COURSE)
    span = brand_block.xpath(".//span")
    if span:
        set_text(span[0], str(cfg["unit"]))
    add_assets(head)
    add_scripts(body)
    for node in root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " route ")]'):
        node.set("class", "box info")
    for node in root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " viz-panel ")]'):
        node.set("class", "box info")
    for node in root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " viz-grid ")]'):
        node.set("class", "grid")
    for node in root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " viz-cell ")]'):
        node.set("class", "box")
    for node in root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " review-card ")]'):
        node.set("class", "box")
    for node in root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " lesson-block ")]'):
        node.set("class", "box soft")
    for node in root.xpath('//p[contains(concat(" ", normalize-space(@class), " "), " can-do ")]'):
        node.set("class", "box soft")
    for node in root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " inline-note ")]'):
        node.set("class", "box warn")


def update_codebars(root: etree._Element, page_prefix: str) -> None:
    codebars = root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " codebar ")]')
    for index, bar in enumerate(codebars, start=1):
        label = first_text(bar, "./span[1]")
        if not label:
            label = f"{page_prefix} 代码 {index}"
        pre = find_direct_next_element(bar, "pre")
        if pre is None:
            continue
        pre_id = pre.get("id") or f"{page_prefix.lower()}_code_{index}"
        pre.set("id", pre_id)
        pre.set("data-export-context", label)
        pre.set("data-export-lang", "python")
        code = pre.xpath(".//code")
        if code:
            ensure_class(code[0], "language-python")
        button = bar.xpath(".//button")[0] if bar.xpath(".//button") else None
        if button is not None:
            button.set("type", "button")
            ensure_class(button, "copy")
            button.set("data-copy", pre_id)


def update_tables(root: etree._Element, cfg: dict[str, object]) -> None:
    trace_table = root.xpath('//section[@id="trace"]//table')
    if trace_table:
        table = trace_table[0]
        table.set("data-export-context", str(cfg["trace"]))
        table.set("data-export-lang", "table")
    for idx, table in enumerate(root.xpath('//section[@id="terms"]//table'), start=1):
        table.set("data-export-context", f"术语表 {idx}")
        table.set("data-export-lang", "table")


def update_formula(root: etree._Element, cfg: dict[str, object]) -> None:
    formulas = root.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " formula ")]')
    for formula in formulas:
        formula.set("class", "math-block")
        formula.set("data-export-context", str(cfg["formula"]))
        formula.set("data-export-lang", "math")


def update_trace_block(root: etree._Element, cfg: dict[str, object]) -> None:
    map_section = root.xpath('//section[@id="map"]')
    if not map_section:
        return
    section = map_section[0]
    tracer = make_shape_tracer(cfg["shape"])
    viz_panel = section.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " viz-panel ")]')
    if viz_panel:
        insert_after(viz_panel[0], tracer)
    else:
        section.append(tracer)


def build_worked_section(cfg: dict[str, object]) -> etree._Element:
    section = etree.Element("section", attrib={"id": "worked-example"})
    head = etree.SubElement(section, "div", attrib={"class": "head"})
    title = etree.SubElement(head, "h2")
    title.text = "完整样例"
    tag = etree.SubElement(head, "span", attrib={"class": "tag"})
    tag.text = "一条完整教学链"

    intro_box = etree.SubElement(section, "div", attrib={"class": "box soft"})
    intro_head = etree.SubElement(intro_box, "h3")
    intro_head.text = str(cfg["worked_title"])
    for para in cfg["worked_intro"]:
        p = etree.SubElement(intro_box, "p")
        p.text = para

    grid = etree.SubElement(section, "div", attrib={"class": "grid2"})
    left = etree.SubElement(grid, "div", attrib={"class": "box info"})
    left_head = etree.SubElement(left, "h3")
    left_head.text = "输入和输出怎么对齐"
    left_para = etree.SubElement(left, "p")
    left_para.text = "先把输入 shape、标签 dtype、输出维度和训练目标写成同一张账本，后面再看 API。"
    right = etree.SubElement(grid, "div", attrib={"class": "box warn"})
    right_head = etree.SubElement(right, "h3")
    right_head.text = "最常见的失配"
    right_para = etree.SubElement(right, "p")
    right_para.text = "这类页最常见的问题不是算不动，而是输入和输出的约定写反。先查 shape，再查 dtype，最后才查 loss。"

    table_wrap = etree.SubElement(section, "div", attrib={"class": "table-wrap"})
    table = etree.SubElement(table_wrap, "table", attrib={"data-export-context": f"{cfg['worked_title']} 账本", "data-export-lang": "table"})
    thead = etree.SubElement(table, "thead")
    header_row = etree.SubElement(thead, "tr")
    for text in ("对象", "shape / 语义", "要读什么", "常见失配"):
        th = etree.SubElement(header_row, "th")
        th.text = text
    tbody = etree.SubElement(table, "tbody")
    for row in cfg["worked_table"]:
        tr = etree.SubElement(tbody, "tr")
        for cell in row:
            td = etree.SubElement(tr, "td")
            td.text = cell

    codebar = etree.SubElement(section, "div", attrib={"class": "codebar"})
    label = etree.SubElement(codebar, "span")
    label.text = "最小可执行片段"
    button = etree.SubElement(codebar, "button", attrib={"class": "copy", "type": "button"})
    button.text = "复制"
    pre = etree.SubElement(section, "pre", attrib={"id": f"{cfg['unit'].split()[0]}_worked_code", "data-export-context": str(cfg["worked_title"]), "data-export-lang": "python"})
    code = etree.SubElement(pre, "code", attrib={"class": "language-python"})
    code.text = str(cfg["worked_code"])

    note = etree.SubElement(section, "div", attrib={"class": "box warn"})
    note_head = etree.SubElement(note, "h3")
    note_head.text = "故障现场"
    note_para = etree.SubElement(note, "p")
    note_para.text = "如果你看到训练能跑但结论不稳，先回到这个样例把 logits、标签和 shape 再核一次。"
    return section


def build_bridge_section(cfg: dict[str, object]) -> etree._Element:
    section = etree.Element("section", attrib={"id": "bridge-chain"})
    head = etree.SubElement(section, "div", attrib={"class": "head"})
    title = etree.SubElement(head, "h2")
    title.text = "故障链"
    tag = etree.SubElement(head, "span", attrib={"class": "tag"})
    tag.text = "从症状回到接口"

    intro = etree.SubElement(section, "div", attrib={"class": "box soft"})
    intro_head = etree.SubElement(intro, "h3")
    intro_head.text = str(cfg["bridge_title"])
    for para in cfg["bridge_paras"]:
        p = etree.SubElement(intro, "p")
        p.text = para

    table_wrap = etree.SubElement(section, "div", attrib={"class": "table-wrap"})
    table = etree.SubElement(table_wrap, "table", attrib={"data-export-context": f"{cfg['bridge_title']} 账本", "data-export-lang": "table"})
    thead = etree.SubElement(table, "thead")
    header = etree.SubElement(thead, "tr")
    for text in ("症状", "你先查什么", "为什么先查它", "修法"):
        th = etree.SubElement(header, "th")
        th.text = text
    tbody = etree.SubElement(table, "tbody")
    for row in cfg["bridge_table"]:
        tr = etree.SubElement(tbody, "tr")
        for cell in row:
            td = etree.SubElement(tr, "td")
            td.text = cell

    codebar = etree.SubElement(section, "div", attrib={"class": "codebar"})
    label = etree.SubElement(codebar, "span")
    label.text = "故障排查片段"
    button = etree.SubElement(codebar, "button", attrib={"class": "copy", "type": "button"})
    button.text = "复制"
    pre = etree.SubElement(section, "pre", attrib={"id": f"{cfg['unit'].split()[0]}_bridge_code", "data-export-context": str(cfg["bridge_title"]), "data-export-lang": "python"})
    code = etree.SubElement(pre, "code", attrib={"class": "language-python"})
    code.text = str(cfg["bridge_code"])

    closing = etree.SubElement(section, "div", attrib={"class": "box info"})
    closing_head = etree.SubElement(closing, "h3")
    closing_head.text = "练习时的用法"
    closing_para = etree.SubElement(closing, "p")
    closing_para.text = "先把上面的症状、表格和代码各读一遍，再回到练习区。这样你写答案时不是在猜，而是在复述已经排过的链路。"
    return section


def build_appendix_section(cfg: dict[str, object]) -> etree._Element:
    section = etree.Element("section", attrib={"id": "consistency-note"})
    head = etree.SubElement(section, "div", attrib={"class": "head"})
    title = etree.SubElement(head, "h2")
    title.text = "一致性补充"
    tag = etree.SubElement(head, "span", attrib={"class": "tag"})
    tag.text = "把接口写稳"

    intro = etree.SubElement(section, "div", attrib={"class": "box info"})
    intro_head = etree.SubElement(intro, "h3")
    intro_head.text = "学习时的落点"
    intro_para = etree.SubElement(intro, "p")
    intro_para.text = "这一段不是再讲一遍前文，而是把训练、评估、调试和迁移时应该固定住的检查顺序收束成一张表。"
    for para in cfg["appendix_paras"]:
        p = etree.SubElement(intro, "p")
        p.text = para

    table_wrap = etree.SubElement(section, "div", attrib={"class": "table-wrap"})
    table = etree.SubElement(table_wrap, "table", attrib={"data-export-context": f"{cfg['appendix_title']} 账本", "data-export-lang": "table"})
    thead = etree.SubElement(table, "thead")
    header = etree.SubElement(thead, "tr")
    for text in ("场景", "先看什么", "为什么", "下一步"):
        th = etree.SubElement(header, "th")
        th.text = text
    tbody = etree.SubElement(table, "tbody")
    for row in cfg["appendix_table"]:
        tr = etree.SubElement(tbody, "tr")
        for cell in row:
            td = etree.SubElement(tr, "td")
            td.text = cell

    codebar = etree.SubElement(section, "div", attrib={"class": "codebar"})
    label = etree.SubElement(codebar, "span")
    label.text = "收束后的检查脚本"
    button = etree.SubElement(codebar, "button", attrib={"class": "copy", "type": "button"})
    button.text = "复制"
    pre = etree.SubElement(section, "pre", attrib={"id": f"{cfg['unit'].split()[0]}_appendix_code", "data-export-context": str(cfg["appendix_title"]), "data-export-lang": "python"})
    code = etree.SubElement(pre, "code", attrib={"class": "language-python"})
    code.text = str(cfg["appendix_code"])

    tip = etree.SubElement(section, "div", attrib={"class": "box warn"})
    tip_head = etree.SubElement(tip, "h3")
    tip_head.text = "最后一遍检查"
    tip_para = etree.SubElement(tip, "p")
    tip_para.text = "把这页的表、代码和练习题一起读完后，再回头看题目。这样你写答案时不是照搬模板，而是在复述一整条已验证过的数据流。"
    return section


def update_questions(root: etree._Element, cfg: dict[str, object]) -> None:
    practice = root.xpath('//section[@id="practice"]')
    if not practice:
        return
    practice = practice[0]
    groups = {}
    for group in practice.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " practice-group ")]'):
        heading = first_text(group, './/div[contains(concat(" ", normalize-space(@class), " "), " group-head ")]//h3[1]')
        groups[group] = heading
    q_nodes = practice.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " q ")]')
    for index, q in enumerate(q_nodes, start=1):
        name = first_text(q, './/input[1]/@name')
        if not name:
            name = f"q{index}"
        q.set("data-question", name)
        group_node = q.xpath('ancestor::div[contains(concat(" ", normalize-space(@class), " "), " practice-group ")][1]')
        if group_node:
            q.set("data-group", groups.get(group_node[0], "练习"))
        title = first_text(q, ".//h3[1]")
        if title:
            q.set("data-title", title)
        note = first_text(q, './/div[contains(concat(" ", normalize-space(@class), " "), " solve-note ")]')
        textareas = q.xpath(".//textarea")
        radios = q.xpath('.//input[@type="radio"]')
        texts = q.xpath('.//input[@type="text"]')

        if radios:
            answer = str(cfg["answers"].get(name, ""))
            if answer:
                q.set("data-answer", answer)
            if note:
                q.set("data-explain", note)
            if not q.xpath('.//button[contains(concat(" ", normalize-space(@class), " "), " check ")]'):
                q.append(etree.Element("button", attrib={"class": "check", "type": "button"}))
                q[-1].text = "检查"
            if not q.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " feedback ")]'):
                q.append(etree.Element("div", attrib={"class": "feedback"}))
            continue

        if texts:
            field = texts[0]
            answer = str(cfg["answers"].get(name, ""))
            if answer:
                field.set("data-answer", answer)
            explain = str(cfg["explain"].get(name, note))
            if explain:
                field.set("data-explain", explain)
            if not q.xpath('.//button[contains(concat(" ", normalize-space(@class), " "), " check ")]'):
                button = etree.Element("button", attrib={"class": "check", "type": "button"})
                button.text = "检查"
                field.addnext(button)
            if not q.xpath('.//div[contains(concat(" ", normalize-space(@class), " "), " feedback ")]'):
                feedback = etree.Element("div", attrib={"class": "feedback"})
                (q.xpath('.//button[contains(concat(" ", normalize-space(@class), " "), " check ")]')[0]).addnext(feedback)
            continue

        if textareas:
            note_text = str(cfg["detail"])
            if not q.xpath('.//button[contains(concat(" ", normalize-space(@class), " "), " reveal ")]'):
                button, details = make_reveal_details(note_text)
                textarea = textareas[0]
                textarea.addnext(details)
                textarea.addnext(button)
            continue


def normalize_source_notes(root: etree._Element) -> None:
    source_items = root.xpath('//section[@id="sources"]//li')
    if source_items:
        first = source_items[0]
        link = first.xpath(".//a[1]")
        if link:
            link = link[0]
            link.text = "来源说明.md"
            first.text = None
            if len(first):
                first.tail = None
            if not first.xpath("string(.)").strip().endswith("教学意图。"):
                link.tail = "：本页的来源说明、锚点样本和教学意图。"


def transform_page(path: Path, cfg: dict[str, object]) -> None:
    text = path.read_text(encoding="utf-8")
    root = html.document_fromstring(text)
    clean_inline_assets(root)
    update_head_body(root, cfg)
    update_codebars(root, cfg["unit"].split()[0])
    update_tables(root, cfg)
    update_formula(root, cfg)
    update_trace_block(root, cfg)
    practice = root.xpath('//section[@id="practice"]')
    if practice:
        if not root.xpath('//section[@id="worked-example"]'):
            insert_before(practice[0], build_worked_section(cfg))
        if not root.xpath('//section[@id="bridge-chain"]'):
            insert_before(practice[0], build_bridge_section(cfg))
        if not root.xpath('//section[@id="consistency-note"]'):
            insert_before(practice[0], build_appendix_section(cfg))
    update_questions(root, cfg)
    normalize_source_notes(root)
    output = "<!doctype html>\n" + html.tostring(root, encoding="unicode", method="html", pretty_print=False)
    path.write_text(output, encoding="utf-8", newline="")


def update_manifest(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    source = data.get("paths", {}).get("source_pack")
    if isinstance(source, str) and source.endswith("source-pack.md"):
        data["paths"]["source_pack"] = source.replace("source-pack.md", "来源说明.md")
    commands = data.get("commands", {})
    for key in ("preflight", "render", "lint"):
        cmd = commands.get(key)
        if isinstance(cmd, list):
            commands[key] = [
                item.replace("source-pack.md", "来源说明.md") if isinstance(item, str) else item
                for item in cmd
            ]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="")


def main() -> int:
    for key, cfg in PAGE_CONFIG.items():
        transform_page(cfg["path"], cfg)
    for key in PAGE_CONFIG:
        update_manifest(PAGE_CONFIG[key]["path"].with_name("_learning-kit-run-manifest.json"))
    print("mixed study pages migrated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
