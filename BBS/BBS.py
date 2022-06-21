"""
BBS伪随机数算法
"""
from random import randint
import Miller_Rabin


# 生成一个大数，并使用miller_rabin判定是否为质数
def getBigPrime():
    """
    取得大质数
    :return:一个512以上二进制位的大质数
    """
    rnd = 0
    for i in range(512):  # 512个二进制位
        rnd = rnd * 2 + randint(0, 1)
    p = rnd * 4 + 3

    if Miller_Rabin.miller_rabin_api(p):
        return p
    while True:
        rnd += 1
        p = rnd * 4 + 3
        if Miller_Rabin.miller_rabin_api(p):
            return p


def BBS(num):
    """
    BBS伪随机数算法
    :param num: 生成伪随机数的比特位数
    :return: 伪随机数（01比特串）
    """
    p = getBigPrime()
    q = getBigPrime()
    while p == q:  # p和q不能相等
        q = getBigPrime()
    n = p * q
    print("p={0}\nq={1}".format(p, q))
    s = randint(0, int(pow(2, randint(0, 4) + 8)))
    while (s % p == 0) or (s % q == 0):  # s与n即p、q互素
        s = randint(0, int(pow(2, randint(4) + 8)))
    x = (s * s) % n
    res = []
    print("生成的伪随机串：", end='')
    for i in range(num):
        x = (x * x) % n
        bbs_i = x % 2
        res.append(bbs_i)
        print(bbs_i, end='')
    """
    test:
    p = 30000000091
    q = 40000000003
    s = 4295260440
    """
    return res


if __name__ == '__main__':
    print("--------BBS伪随机数算法--------")
    num = eval(input("请输入生成随机数的位数："))
    res = BBS(num)

