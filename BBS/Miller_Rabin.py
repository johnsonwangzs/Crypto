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
    T = 100  # 检测次数
    flag = 1  # 质数标记
    while T > 0:
        T = T - 1
        if not miller_rabin(N):  # 是合数
            flag = 0
            return False
    if flag == 1:
        return True


def main():
    n = eval(input("Please enter the number N to be tested:"))

    # n=1000023
    # n=1000033
    # n=100160063
    # n=1500450271
    # n=1494462659429290047815067355171411187560751791530
    # n=22490812876539885046336053040043361022772062226905764414319531416752624982967181455912526153033030222985778230314070837549143068021815197910334221004333099
    # n=173114538715442253801652636578504897235814058376012019984132280493073144140873423822066926533851768593567972986030786930865304524765873917291156820356593465395949615668311730524585862713216977118030162614331116320577533153712280997129347743623082819252354000224098702300466561157715990374851814717133985999661

    if miller_rabin_api(n):
        print("质数！")
    else:
        print("合数！")


if __name__ == '__main__':
    main()
