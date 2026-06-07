# 02 · Autograd（自动求导）

## 计算图

PyTorch 在执行张量运算时隐式构建 DAG，每个操作记录 `grad_fn`。调用 `backward()` 时沿图反向传播，链式法则自动计算所有叶子节点的梯度。

## backward()

- 只能对**标量**调用（shape 为 `()` 或 `[1]`）；非标量需传 `gradient` 参数
- 梯度存入叶子节点的 `.grad`，中间节点不保留
- 梯度**累加**（非覆盖）——每次 backward 把新梯度加到旧梯度上，不会自动清零

> [!info] 梯度为什么设计成累加
> 为了支持**梯度累积**：显存不够跑大 batch 时，多次小 batch 分别 backward（梯度自动累加），然后统一更新一次参数——数学上等价于一次大批次训练。

## 最小代码模板

```python
import torch

w = torch.tensor([10.0], requires_grad=True)
x = torch.tensor([3.0])
target = torch.tensor([12.0])

y_pred = w * x
loss = (y_pred - target) ** 2
loss.backward()

with torch.no_grad():
    w -= 0.05 * w.grad

w.grad = None  # 清零
```

## no_grad vs detach vs zero_

最易串的三个概念：

| 操作 | 本质 | 适合场景 |
|------|------|---------|
| `with torch.no_grad():` | **开关**——包住一段代码，区域内全部不建图 | 推理、评估、参数更新 |
| `tensor.detach()` | **切绳子**——返回一个值相同但脱离图的新张量 | 取出中间值做别的事（打印、保存），又不想影响梯度 |
| `tensor.grad = None` 或 `.zero_()` | **清零**——把 `.grad` 属性归零 | 每次更新完参数后必须做，否则下次 backward 会累加 |

> [!warning] 混淆记录
> 第 6 题填空：`zero_` 填成了 `no_grad`，`None` 填成了 `detach`。
> 第 7 题：`no_grad()` 填成了 `grad()`。
> — 这三个见一次错一次，硬记：**no_grad 是开关，detach 切绳子，zero_/None 清梯度。**

> [!tip] 参数更新必须包在 no_grad 里
> `w -= lr * w.grad` 如果不在 no_grad 下执行，这步减法本身也会被记入计算图，图越滚越大。

## 三个限制

- `requires_grad=True` 的张量**必须是浮点或复数类型**；`torch.tensor([3])` 默认 int64 会报错，必须写 `[3.0]`
- `backward()` 只能对**标量**调用；对向量/矩阵调用需传 `gradient` 参数
- 同一个计算图只能 backward **一次**（除非 `retain_graph=True`），否则报错

> [!warning] 批卷踩坑记录
> `torch.tensor([3,0])` 逗号误打成两个整数元素，且 int 类型不能 requires_grad——正确写法 `torch.tensor([3.0], requires_grad=True)`

## 费曼解释

> 你手写训练代码时，每算一次 loss 都要自己推导 ∂loss/∂w、∂loss/∂b 的公式——参数少还行，1000 万参数时根本不可能。PyTorch 的 autograd 相当于在背后自动画了一张"运算流水图"，你只要写前向传播的代码，然后调用 `backward()`，它沿着图反向用链式法则一次性算出所有参数的梯度。梯度会自动累加到 `.grad` 属性里等着你去取——就像你在餐厅点菜，不需要自己进厨房切菜炒菜，只需要下单（前向），服务员把菜端回来（backward），你就拿到了每个菜（梯度）。

## 术语速查

| 术语 | 代码/含义 |
|------|---------|
| 标记求导 | `requires_grad=True` |
| 反向求导 | `loss.backward()` |
| 读梯度 | `w.grad` |
| 清零梯度 | `w.grad = None`（推荐）或 `w.grad.zero_()` |
| 推理模式 | `with torch.no_grad():` |
| 切断梯度 | `t.detach()` |
| 叶子节点 | 直接创建的 `requires_grad=True` 张量，backward 后保留 `.grad` |
