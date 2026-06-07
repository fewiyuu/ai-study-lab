---
title: "04 · Module 与优化器"
aliases:
  - PyTorch Module 与优化器
  - PyTorch 训练 step
tags:
  - 深度学习
  - PyTorch
  - course-forge
  - 训练循环
---

> [!question] 常见问题速查
> - 训练代码里，哪一行真的改了参数？
> - `loss.backward()` 会不会更新参数？
> - `.grad` 是谁写进去的，又是谁读取的？
> - 为什么每个 batch 前通常要 `zero_grad()`？
> - 为什么 `CrossEntropyLoss` 前通常不手动 softmax？
> - optimizer 创建后再替换模型层，会发生什么？
> - 普通 Python list 里放子层，`model.parameters()` 能找到吗？
> - `model.eval()` 和 `torch.no_grad()` 到底差在哪？
> - 验证集 loss 能正常算出来，为什么还要关梯度？

> [!abstract] 核心主线
> PyTorch 训练不是一段固定咒语，而是几个对象在传递状态：`nn.Module` 注册参数，`model(x)` 触发 `forward`，loss 把预测错误压成标量张量，`backward()` 把梯度写进参数 `.grad`，`optimizer.step()` 读取 `.grad` 并原地更新参数。

```text
Module 注册参数
→ model(x) 触发 forward
→ loss 把预测错误压成标量张量
→ backward 把梯度写进参数 .grad
→ optimizer.step 读取 .grad 并原地更新参数
```

> [!tip] 最关键的判断
> `loss.backward()` 只计算梯度并写入 `.grad`；真正修改参数值的是 `optimizer.step()`。

## 概念精讲

### nn.Module：模型为什么能知道自己有哪些参数

`nn.Module` 不是只让代码更整齐的基类。它的关键作用是管理模型里的子层、参数和状态。

在 `__init__` 里把子层挂到 `self` 上，例如 `self.linear = nn.Linear(...)`，PyTorch 会把这个子层注册为当前模块的一部分。之后调用 `model.parameters()` 时，PyTorch 会递归找到这些子层里的权重和偏置。

如果你自己创建可训练权重，通常要写成 `nn.Parameter`，再挂到 `self` 上。普通 `Tensor` 不会自动进入参数列表；不进入参数列表，优化器就拿不到，也就不会更新。

> [!warning] 常见坑：普通 list 不注册子层
> ```python
> self.layers = [nn.Linear(10, 10), nn.ReLU(), nn.Linear(10, 1)]
> ```
>
> 这种 list 里的子层不会被稳定注册。应该改成 `nn.ModuleList`、`nn.Sequential`，或者把子层逐个挂到 `self.xxx`。

### forward 与 model(x)：写 forward，调用 model(x)

`forward` 定义输入如何变成输出。日常使用模型时，不直接调 `forward`，而是写：

```python
pred = model(x)
```

`model(x)` 会进入 `nn.Module.__call__`，再调用你写的 `forward`。这个入口会处理 hook、框架封装、模式管理等机制。直接写 `model.forward(x)` 在简单例子里可能能跑，但工程上不稳。

### loss：反向传播的入口

loss 不是普通数字，而是带计算图的张量。训练里常要求 loss 是标量张量，因为反向传播需要一个明确的起点。

```python
loss = criterion(pred, y)
loss.backward()
```

这里的 `loss` 通常形如 `tensor(0.73, grad_fn=...)`。它只有一个值，但仍然连着计算图。调用 `backward()` 后，PyTorch 才能从这个标量目标一路反向算到模型参数。

如果 loss 不是标量，直接 `backward()` 可能报错，或者需要显式传入外部梯度。

### CrossEntropyLoss：通常吃 logits

多分类任务里，`nn.CrossEntropyLoss` 通常接收 logits 和类别编号。

```python
criterion = nn.CrossEntropyLoss()
logits = model(x)
loss = criterion(logits, target)
```

> [!important] 不要手动 softmax
> `CrossEntropyLoss` 内部已经包含 `log_softmax + NLLLoss`。提前 softmax 会改变它期望的输入形式，也会让数值稳定性变差。

### zero_grad、backward、step：三件事不能互相替代

PyTorch 默认会累积梯度。也就是说，如果不清空 `.grad`，下一轮 `backward()` 算出的梯度会加到旧梯度上。

| 动作 | 做什么 | 不做什么 |
|---|---|---|
| `optimizer.zero_grad()` | 清掉旧梯度 | 不改参数 |
| `loss.backward()` | 计算梯度，写入 `.grad` | 不更新参数 |
| `optimizer.step()` | 读取 `.grad`，更新参数 | 不重新计算梯度 |

标准顺序通常是：

```text
zero_grad → forward → loss → backward → step
```

除非你有意做梯度累积，否则每个 mini-batch 更新前通常要先清梯度。

### optimizer：持有参数引用，不会自动发现新层

创建优化器时：

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
```

优化器拿到的是参数对象的引用，不是参数副本。`loss.backward()` 把梯度写到这些参数的 `.grad`，`optimizer.step()` 再读取 `.grad` 并更新参数值。

> [!bug] 替换层之后，旧 optimizer 不会自动更新
> ```python
> optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
> model.head = nn.Linear(768, 10)  # 新 head 不在旧 optimizer 里
> ```
>
> 更稳的顺序是先替换层，再创建优化器。

### SGD 与 Adam：一个更直接，一个更自适应

| 优化器 | 直觉 | 常见特点 |
|---|---|---|
| SGD | 按当前梯度方向更新，学习率控制基础步长 | 更直接，学习率更敏感；带 momentum 时会利用历史方向 |
| Adam | 维护梯度的一阶和二阶统计量，给不同参数自适应调整更新幅度 | 常更省调参，前期收敛更快，但不保证泛化一定更好 |

### train、eval、no_grad：名字像一组，其实管不同东西

| 写法 | 控制什么 | 典型影响 | 不能替代什么 |
|---|---|---|---|
| `model.train()` | 模型进入训练模式 | Dropout 随机丢弃，BatchNorm 用当前 batch 统计 | 不负责更新参数 |
| `model.eval()` | 模型进入评估模式 | Dropout 关闭随机丢弃，BatchNorm 用累计统计 | 不关闭梯度记录 |
| `torch.no_grad()` | 关闭计算图记录 | 省显存、少计算 | 不改变模型模式 |

验证阶段常见组合是：

```python
model.eval()
with torch.no_grad():
    ...
```

> [!tip] 排查顺序
> 验证指标在有 Dropout 的模型上异常波动，先查 `model.eval()`。验证阶段显存持续上涨，先查 `torch.no_grad()`，以及是否把带计算图的 `pred`、`loss` 存进列表。

## 最小可操作样例

### 最小 Module

```python
import torch
from torch import nn

class TinyRegressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
        )

    def forward(self, x):
        return self.net(x)

model = TinyRegressor()
print(sum(p.numel() for p in model.parameters()))
```

这个例子要看三点：

- `super().__init__()` 初始化 Module 的内部登记系统。
- `self.net = ...` 把子模块挂到模型上。
- `model.parameters()` 能递归找到 `Linear` 里的权重和偏置。

### 标准训练 step

```python
model.train()

for x, y in train_loader:
    optimizer.zero_grad()
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
```

> [!warning] 删掉任意关键行，后果都不同
> - 删 `zero_grad()`：梯度持续累积。
> - 删 `loss.backward()`：本轮没有正确梯度。
> - 删 `optimizer.step()`：参数不会更新。

### 验证模板

```python
model.eval()
val_loss = 0.0

with torch.no_grad():
    for x, y in val_loader:
        pred = model(x)
        loss = criterion(pred, y)
        val_loss += loss.item()
```

验证阶段一般不应该出现：

```python
loss.backward()
optimizer.step()
```

### 只微调最后一层

```python
for p in model.backbone.parameters():
    p.requires_grad = False

model.head = nn.Linear(in_features, num_classes)
optimizer = torch.optim.Adam(model.head.parameters(), lr=1e-3)
```

## 关键术语 / 符号 / 框架

| 术语 | 准确含义 | 容易混淆的点 |
|---|---|---|
| `nn.Module` | PyTorch 模型基类，负责管理子层、参数和状态 | 不是只为了代码好看 |
| `nn.Parameter` | 会被 Module 注册为可训练参数的 Tensor 包装 | 普通 Tensor 不会自动进入 `parameters()` |
| `model.parameters()` | 返回模型已注册参数的迭代器 | 不是复制参数，而是暴露参数对象 |
| `forward` | 定义输入到输出的计算逻辑 | 日常调用应写 `model(x)` |
| logits | softmax 前的原始分类分数 | `CrossEntropyLoss` 通常吃 logits |
| scalar loss | 只有一个值、且连着计算图的张量 | 不是 Python float |
| `.grad` | 参数上的梯度缓存 | `backward()` 写入，`step()` 读取 |

## 判断与行动清单

> [!todo] 验收一段 PyTorch 训练代码
> - [ ] 模型参数是否被注册：子层挂到 `self` 上了吗？多层容器是否用 `ModuleList` 或 `Sequential`？
> - [ ] optimizer 是否拿到正确参数：替换层之后才创建 optimizer 吗？只微调时是否只传目标层参数？
> - [ ] step 顺序是否完整：`zero_grad → model(x) → loss → backward → step` 有没有缺？
> - [ ] loss 是否匹配任务：输出形状、标签格式、loss 函数是否匹配？
> - [ ] 是否误用 softmax：`CrossEntropyLoss` 前是否手动 softmax？
> - [ ] 梯度和参数是否真的变化：`.grad` 是否为 None？`step()` 后目标参数是否变化？
> - [ ] 验证是否干净：`model.eval()` 和 `torch.no_grad()` 是否都用了？
> - [ ] 日志是否断图：`loss.item()` 是否只用于记录，而不是拿去反向传播？

## 应用与迁移问答

### 训练代码里哪一行真的改了参数？

`optimizer.step()`。`loss.backward()` 只计算梯度并写入 `.grad`，真正修改参数值的是 optimizer 的 `step()`。

### loss.item() 后还能 backward 吗？

不能对 `loss.item()` 的结果调用 `backward()`，因为它已经变成 Python 数字，计算图断了。

但如果原始 `loss` 张量还在，仍然可以：

```python
loss.backward()
```

错误写法是：

```python
loss_value = loss.item()
loss_value.backward()
```

### optimizer 创建后又替换 model.head 会怎样？

旧 optimizer 仍然拿着旧参数引用，新 head 的参数不会自动加入优化器。结果可能是前向用新 head，但 optimizer 更新的不是你以为的那批参数。

修法：先替换层，再创建 optimizer；或者把新参数加入 optimizer 的 param group。

### 如果验证集指标波动很大，先查什么？

如果模型里有 Dropout 或 BatchNorm，先查是否忘了 `model.eval()`。如果验证阶段显存越来越高，先查是否忘了 `torch.no_grad()`。

### 只微调最后一层时，优化器参数怎么传？

只传最后一层参数：

```python
optimizer = torch.optim.Adam(model.head.parameters(), lr=1e-3)
```

同时检查其他层是否冻结、新 head 是否已替换完成、optimizer 是否在替换后创建。

## 练习 / 盲区复盘

> [!failure] 盲区 1：loss 标量的作用
> 原答卷把标量 loss 理解成“方便比较是否最优”。更准确的说法是：标量 loss 是反向传播的明确起点。它是带计算图的单值张量，调用 `backward()` 后，PyTorch 才能从 loss 回到参数梯度。

> [!failure] 盲区 2：CrossEntropyLoss 不手动 softmax 的原因
> 正确原因是：`CrossEntropyLoss` 内部已经包含 `log_softmax + NLLLoss`，输入应该是 logits。提前 softmax 会破坏数值稳定性，也不符合这个 loss 的预期输入。

> [!failure] 盲区 3：代码诊断顺序
> 错误代码缺少 `loss.backward()`，而且 `optimizer.step()` 出现在反向传播之前。标准顺序应是 `zero_grad → forward → loss → backward → step`。

> [!failure] 盲区 4：普通 list 保存层
> 普通 Python list 不会让里面的 `nn.Module` 自动注册。`model.parameters()` 可能找不到这些层里的参数，优化器也就无法更新它们。

> [!failure] 盲区 5：微调最后一层
> 应明确传最后一层参数：`optimizer = torch.optim.Adam(model.head.parameters(), lr=1e-3)`。同时检查其他层是否冻结，新 head 是否已替换完成，optimizer 是否在替换后创建。

## 费曼解释润色版

> [!quote]
> 一次训练 step 开始前，模型继承 `nn.Module`，子层和参数会被注册到 `model.parameters()` 里，优化器拿到的是这些参数的引用。每个 batch 更新前，先调用 `optimizer.zero_grad()` 清掉上一轮留在参数 `.grad` 上的梯度。然后用 `model(x)` 做前向传播，它会进入模型的 `forward`，得到预测结果。loss 函数把预测和标签的差异聚合成一个标量张量，并保留从 loss 回到参数的计算图。调用 `loss.backward()` 后，PyTorch 沿计算图反向计算，把每个参数对应的梯度写入参数的 `.grad`。最后 `optimizer.step()` 读取这些 `.grad`，按 SGD 或 Adam 的规则原地修改参数值。下一次 `model(x)` 会使用更新后的参数。训练阶段通常用 `model.train()`，验证阶段通常用 `model.eval()` 加 `torch.no_grad()`，避免 Dropout、BatchNorm 行为和梯度记录出错。

## 易错卡片

> [!warning] 误区：loss.item() 之后还能反向传播
> 正确说法：`loss.item()` 得到的是 Python 数字，不能 `backward()`；只有原始 loss 张量保留计算图。
>
> 提醒：记录日志用 `loss.item()`，训练反向用 `loss.backward()`。

> [!warning] 误区：optimizer 拥有模型参数
> 正确说法：optimizer 持有参数引用，参数本体仍在模型里。
>
> 提醒：替换模型层后，要重新创建 optimizer 或添加新参数组。

> [!warning] 误区：backward 会更新参数
> 正确说法：`backward()` 只写梯度，`step()` 才更新参数。
>
> 提醒：看到训练不动时，同时检查是否有 `backward()` 和 `step()`。

> [!warning] 误区：eval 会自动关闭梯度
> 正确说法：`eval()` 改模型行为，`no_grad()` 关计算图记录。
>
> 提醒：验证阶段常用 `model.eval()` + `with torch.no_grad():`。

> [!warning] 误区：list 里的层会自动注册
> 正确说法：普通 Python list 不会自动注册子模块。
>
> 提醒：保存多个层时优先用 `nn.ModuleList` 或 `nn.Sequential`。
