from random import randint


def miller_rabin(n):
    if n % 2 == 0:
        return False
    if n == 1:
        return False
    if n == 2:
        return True
    q = n - 1
    k = 0
    while q % 2 == 0:  # (n-1)一直除2，直到q为一个奇数
        q = q // 2
        k = k + 1
    a = randint(2, n - 1)  # 随机生成一个a
    if fast_pow_mod(a, q, n) == 1:
        return True
    for i in range(0, k):
        p = pow(2, i)
        if fast_pow_mod(a, p * q, n) == n - 1:
            return True
    return False


def fast_pow_mod(x, n, m):
    d = 1
    while n > 0:
        if n % 2 == 1:
            d = (d * x) % m
            n = (n - 1) // 2
        else:
            n = n // 2
        x = (x * x) % m
    return d


def miller_rabin_api(N):
    T = 20  # 检测次数
    flag = 1  # 质数标记
    while T > 0:
        T = T - 1
        if not miller_rabin(N):  # 是合数
            flag = 0
            return False
    if flag == 1:
        return True
