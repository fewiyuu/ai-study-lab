"""
PyTorch 第 03 块：数据加载（Dataset & DataLoader）

用法：
1. 把所有 None 改成你的答案。
2. 运行：uv run python 批卷.py
3. 如果当前目录没有 uv 环境，也可以直接运行：python 批卷.py
"""

import torch
from torch.utils.data import Dataset, DataLoader, TensorDataset


def safe_value(fn, default=None):
    try:
        return fn()
    except Exception:
        return default


# ═══════════════════════════════════════════════════════════════
# 题 1：Dataset 负责“怎么取一条数据”，必须实现 __len__ 和 __getitem__

class TinyPairDataset(Dataset):
    def __init__(self):
        self.x = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
        self.y = torch.tensor([[2.0], [4.0], [6.0], [8.0]])

    def __len__(self):
        return None

    def __getitem__(self, idx):
        return None


# ═══════════════════════════════════════════════════════════════
# 题 2：DataLoader 负责“怎么取一批数据”，batch_size 决定每批大小

q2_batch_size = None
q2_loader = safe_value(lambda: DataLoader(TinyPairDataset(), batch_size=q2_batch_size, shuffle=False))
q2_first_batch = safe_value(lambda: next(iter(q2_loader)))
q2_first_x = safe_value(lambda: q2_first_batch[0])
q2_first_y = safe_value(lambda: q2_first_batch[1])


# ═══════════════════════════════════════════════════════════════
# 题 3：DataLoader 的 batch 数量等于 ceil(样本数 / batch_size)

q3_dataset = TensorDataset(torch.arange(10), torch.arange(10) * 10)
q3_batch_size = None
q3_loader = safe_value(lambda: DataLoader(q3_dataset, batch_size=q3_batch_size, shuffle=False))
q3_num_batches = None
q3_last_batch_size = None


# ═══════════════════════════════════════════════════════════════
# 题 4：drop_last=True 会丢掉最后一个不满 batch

q4_drop_last = None
q4_loader = DataLoader(q3_dataset, batch_size=4, shuffle=False, drop_last=bool(q4_drop_last))
q4_num_batches = None


# ═══════════════════════════════════════════════════════════════
# 题 5：shuffle=True 只改变顺序，不改变 batch 数量和样本总数

q5_loader = DataLoader(q3_dataset, batch_size=5, shuffle=True)
q5_num_batches = None
q5_total_seen = None


# ═══════════════════════════════════════════════════════════════
# 题 6：训练集通常 shuffle=True，验证集通常 shuffle=False

train_loader = DataLoader(q3_dataset, batch_size=2, shuffle=None)
valid_loader = DataLoader(q3_dataset, batch_size=2, shuffle=None)

q6_train_shuffle_should_be = None
q6_valid_shuffle_should_be = None


# ═══════════════════════════════════════════════════════════════
# 题 7：写一个最小训练循环，只负责把 batch 喂给模型并更新参数

linear = torch.nn.Linear(1, 1)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(linear.parameters(), lr=0.01)
train_ds = TensorDataset(
    torch.tensor([[1.0], [2.0], [3.0], [4.0]]),
    torch.tensor([[2.0], [4.0], [6.0], [8.0]]),
)
train_dl = DataLoader(train_ds, batch_size=2, shuffle=False)

q7_losses = []
for xb, yb in train_dl:
    try:
        pred = None
        loss = None
        optimizer.zero_grad()
        None
        optimizer.step()
        q7_losses.append(float(loss.detach()))
    except Exception:
        q7_losses.append(float("nan"))
