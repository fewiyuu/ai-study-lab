---
title: P03 机器学习任务攻略 - 本地来源说明
aliases: []
tags:
  - learning-kit
  - P03
  - source-pack
snapshot: 2026-06-21
---

# P03 机器学习任务攻略｜本地来源说明

## 来源边界

- [课程目录页](../index.html)：确认 P03 在整门课中的位置，以及它和 P02、P04 的前后衔接。
- [课程说明](../README.md)：确认课程命名、目录用途和已完成状态。
- 重构前的 [学习页](./学习页.html)：回收这一节已有的诊断主线、例子、练习方向和代码桥。
- [P02 学习页](../P02_深度学习基本概念简介/学习页.html)：对齐 training / validation / test 的基础术语，避免在 P03 里把深度学习基础说乱。
- [P04 学习页](../P04_局部最小值与鞍点/学习页.html)：作为后续衔接边界，提醒这里先讲任务排查，不展开 critical point、Hessian 或 saddle point。

Snapshot: 本地文件于 2026-06-21 检查。

## 单元范围

- 这一页只讲机器学习任务里的诊断顺序：先看 training loss，再看 validation / testing loss，再决定是 model bias、optimization failure，还是 overfitting。
- 重点对象是 training set、validation set、testing set、public leaderboard、data augmentation、regularization、early stopping 和最小代码桥。
- 不把本页扩成优化理论、梯度下降推导、二阶曲率分析、batch norm 或更后面的结构技巧。

## 重构备注

- 诊断顺序固定为：training loss -> validation loss -> public / private test。
- 同一个锚点例子贯穿全页：训练集好、验证集差，和训练集本来就没学好，是两类不同问题。
- 语言保持直接，不写成“本节将带你……”一类模板句。
- 练习题优先覆盖“怎么判断”和“下一步做什么”，而不是只考名词背诵。
