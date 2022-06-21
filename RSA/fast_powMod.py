import Montgomery


def fast_pow_mod(x, n, m):
    d = 1
    while n > 0:
        if n % 2 == 1:
            d = (d * x) % m  # 将n的二进制表示中等于1的位对应的x的幂相乘
            n = (n - 1) // 2
        else:
            n = n // 2
        x = (x * x) % m  # 计算x的2^i次幂
    return d


def fast_pow_mod_montgomery(x, n, m):
    d = 1
    while n > 0:
        if n % 2 == 1:
            d = Montgomery.montegomery(d, x, m)
            n = (n - 1) // 2
        else:
            n = n // 2
        x = Montgomery.montegomery(x, x, m)
    return d