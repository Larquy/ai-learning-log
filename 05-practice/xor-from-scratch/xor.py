#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""XOR 从零实现（2 → 4 → 1，sigmoid，纯 Python 标准库）

用法：python3 xor.py
骨架说明：函数体留给你写。没实现完也能运行 —— 程序会告诉你还差哪几步。

网络结构：
    输入 2 个 → 隐藏层 4 个（sigmoid）→ 输出 1 个（sigmoid）

数据（就是 XOR，注意它线性不可分，所以必须有隐藏层）：
    输入 (0,0) -> 0
    输入 (0,1) -> 1
    输入 (1,0) -> 1
    输入 (1,1) -> 0

跑通标准：训练后四组输出与 [0,1,1,0] 的误差 < 0.05。
"""
import csv
import math
import os
import random

DATA = [(([0.0, 0.0]), 0.0),
        (([0.0, 1.0]), 1.0),
        (([1.0, 0.0]), 1.0),
        (([1.0, 1.0]), 0.0)]

HIDDEN = 4          # 隐藏层神经元数
LR = 0.5            # 学习率
EPOCHS = 5000       # 训练轮数
SEED = 0            # 固定随机种子，保证可复现


# ---------------------------------------------------------------- ①
def sigmoid(z):
    """TODO: 返回 1/(1+exp(-z))。注意 z 很负时要防止 exp 溢出。"""
    raise NotImplementedError("① sigmoid 还没写")


def sigmoid_deriv(s):
    """TODO: 输入 sigmoid 的输出 s，返回 s*(1-s)（导数用输出表示，省一次计算）。"""
    raise NotImplementedError("① sigmoid 导数还没写")


# ---------------------------------------------------------------- ②
def init_params():
    """TODO: 初始化 W1(4x2)、b1(4)、W2(1x4)、b2(1)，用 random.uniform(-1,1) 之类的小随机数。"""
    raise NotImplementedError("② 参数初始化还没写")


def forward(x, params):
    """TODO: 前向传播。返回 (输出值, 中间量)，中间量里要存好反向传播需要的东西
    （隐藏层激活值、输出层激活值）。"""
    raise NotImplementedError("② 前向传播还没写")


# ---------------------------------------------------------------- ③
def backward(x, y, params, cache):
    """TODO: 反向传播，返回各参数的梯度 (dW1, db1, dW2, db2)。

    提示（链式法则两段）：
      输出层: delta2 = (out - y) * sigmoid_deriv(out)
      隐藏层: delta1 = (delta2 · W2) * sigmoid_deriv(hidden)
    """
    raise NotImplementedError("③ 反向传播还没写")


# ---------------------------------------------------------------- ④
def train():
    """TODO: 主训练循环。每轮：前向 → 算损失(可选) → 反向 → 用 LR 更新参数。

    返回 params 和损失序列 losses（每轮一个数，供画曲线）。
    """
    raise NotImplementedError("④ 训练循环还没写")


# ---------------------------------------------------------------- ⑤
def predict(x, params):
    """TODO: 返回前向传播的输出值（0~1 之间的小数）。"""
    raise NotImplementedError("⑤ 预测还没写")


# ---------------------------------------------------------------- ⑥
def save_loss(losses, path="results/loss.csv"):
    """TODO: 把损失序列写成 csv（列名 epoch,loss），用 csv 模块。"""
    raise NotImplementedError("⑥ 损失记录还没写")


def _missing_steps():
    """探测哪些步骤还没实现（只判断有没有抛 NotImplementedError）。"""
    checks = [
        ("① sigmoid / sigmoid_deriv", lambda: (sigmoid(0.5), sigmoid_deriv(0.5))),
        ("② init_params / forward", lambda: forward([0.0, 0.0], init_params())),
        ("③ backward", lambda: backward([0.0, 0.0], 0.0, None, None)),
        ("④ train", lambda: train()),
        ("⑤ predict", lambda: predict([0.0, 0.0], None)),
        ("⑥ save_loss", lambda: save_loss([], "results/.probe.csv")),
    ]
    missing = []
    for label, fn in checks:
        try:
            fn()
        except NotImplementedError:
            missing.append(label)
        except Exception:
            pass          # 写代码过程中的其它报错，不影响"还缺哪步"的判断
        finally:
            if os.path.exists("results/.probe.csv"):
                os.remove("results/.probe.csv")
    return missing


def main():
    missing = _missing_steps()
    if missing:
        print("XOR 从零实现 —— 还差这几步没写：")
        for t in missing:
            print("   -", t)
        print("\n按 README 的任务清单顺序写；写完再跑：python3 xor.py")
        return

    random.seed(SEED)
    params, losses = train()
    print(f"训练完成：共 {len(losses)} 轮，最终损失 {losses[-1]:.6f}")
    for x, y in DATA:
        print(f"  {x} → {predict(x, params):.4f}   (期望 {y:.0f})")
    save_loss(losses)
    print("损失已写入 results/loss.csv")


if __name__ == "__main__":
    main()
