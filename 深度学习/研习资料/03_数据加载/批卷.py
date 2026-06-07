import math
import os
import runpy
import traceback

import torch


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXERCISE_PATH = os.path.join(BASE_DIR, "习题.py")


def same_tensor(actual, expected):
    return torch.equal(actual, expected)


def grade(name, check, detail):
    try:
        ok = bool(check())
        return ok, f"{'✅' if ok else '❌'} {name}：{detail}"
    except Exception as exc:
        return False, f"❌ {name}：运行出错：{exc}\n{traceback.format_exc(limit=1)}"


def main():
    ns = runpy.run_path(EXERCISE_PATH)
    results = []

    ds = ns["TinyPairDataset"]()

    results.append(grade(
        "题 1 Dataset 基本接口",
        lambda: len(ds) == 4
        and same_tensor(ds[2][0], torch.tensor([3.0]))
        and same_tensor(ds[2][1], torch.tensor([6.0])),
        "__len__ 应返回样本数，__getitem__ 应返回 (x[idx], y[idx])。",
    ))

    results.append(grade(
        "题 2 DataLoader 第一批",
        lambda: ns["q2_first_x"].shape == torch.Size([2, 1])
        and same_tensor(ns["q2_first_x"], torch.tensor([[1.0], [2.0]]))
        and same_tensor(ns["q2_first_y"], torch.tensor([[2.0], [4.0]])),
        "batch_size=2 时第一批应包含前两条样本。",
    ))

    results.append(grade(
        "题 3 batch 数量与最后一批",
        lambda: ns["q3_num_batches"] == 4 and ns["q3_last_batch_size"] == 1,
        "10 条样本、batch_size=3 时有 4 批，最后一批 1 条。",
    ))

    results.append(grade(
        "题 4 drop_last",
        lambda: len(ns["q4_loader"]) == 2 and ns["q4_num_batches"] == 2,
        "10 条样本、batch_size=4、drop_last=True 时只保留 2 个完整 batch。",
    ))

    results.append(grade(
        "题 5 shuffle 不改变数量",
        lambda: ns["q5_num_batches"] == 2 and ns["q5_total_seen"] == 10,
        "shuffle 只改变顺序，不改变 batch 数量和样本总数。",
    ))

    results.append(grade(
        "题 6 训练/验证 shuffle 习惯",
        lambda: ns["q6_train_shuffle_should_be"] is True
        and ns["q6_valid_shuffle_should_be"] is False,
        "训练集通常打乱，验证集通常不打乱，方便结果可复现和可比较。",
    ))

    results.append(grade(
        "题 7 最小训练循环",
        lambda: len(ns["q7_losses"]) == 2
        and all(math.isfinite(v) and v >= 0 for v in ns["q7_losses"]),
        "每个 batch 应完成 forward、loss、zero_grad、backward、step。",
    ))

    score = sum(ok for ok, _ in results)
    total = len(results)
    print(f"得分：{score}/{total}")
    for _, message in results:
        print(message)

    if score == total:
        print("\n全对。你现在应该能做什么：")
        print("- 自己写一个最小 Dataset。")
        print("- 用 DataLoader 控制 batch_size、shuffle、drop_last。")
        print("- 把 DataLoader 接进最小训练循环。")


if __name__ == "__main__":
    main()

