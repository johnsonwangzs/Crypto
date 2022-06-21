# -*- coding: utf-8 -*-
# @Time     : 2022/6/8 13:46
# @Author   : WZS
# @File     : Montgomery.py
# @Software : PyCharm
# @Function :

import math

import GCD
import extended_GCD


def Multiplicative_inverse_modulo(a, b):
    if b < 0:
        m = abs(b)
    else:
        m = b
    flag = GCD.gcd(a, b)

    if flag == 1:
        gcd, x, y = extended_GCD.extended_gcd(a, b)
        x0 = x % m
        return x0
    else:
        print("Error!")
        exit()


def montegomery(a, b, N):
    R = 2 ** (int(math.log2(N) + 1))

    N1 = Multiplicative_inverse_modulo(N, R)
    N2 = R - N1

    a_ = (a * R) % N
    b_ = (b * R) % N
    c_ = (((a_ * b_) + (((a_ * b_) * N2) % R) * N) // R) % N

    c = (c_ + (c_ * N2) % R * N) // R

    return c

