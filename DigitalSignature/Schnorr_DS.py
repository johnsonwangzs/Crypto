from Miller_Rabin import *
from extended_GCD import *
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def getBigPrime(n):
    """
    取得大质数
    :param n: 生成大质数的位数
    :return:一个n位以上二进制位的大质数
    """
    # rnd = 0
    # for i in range(n):  # 1024个二进制位
    #     rnd = rnd << 1 + randint(0, 1)  # 以16个二进制位为一组，共生成512位
    # rnd = rnd | (1 << (n - 1))  # 保证至少为512二进制位
    rnd = randint(pow(2, n - 1), pow(2, n))
    rnd = rnd | 1  # 保证为奇数

    while True:
        if miller_rabin_api(rnd, 5):
            return rnd
        rnd += 2


def generateKey(p, q, a):
    """
    公私钥生成函数
    :param p: 大质数1024位
    :param q: 大质数160位
    :param a: 整数a
    :return: 公钥v，私钥s
    """
    s = randint(1, q - 1)
    v = extended_gcd(pow(a, s, p), p)[1]

    return s, v


def sign(M, s, puKeyParam):
    """
    签名函数
    :param puKeyParam: 全局公钥参数
    :param M: 待签名消息
    :param s: 私钥
    :return: 签名结果
    """
    a, p, q = puKeyParam[0], puKeyParam[1], puKeyParam[2]
    r = randint(1, q - 1)
    x = fast_pow_mod(a, r, p)
    e = hash(M + str(x))
    y = (r + s * e) % q
    while e < 0:
        r = randint(1, q - 1)
        x = fast_pow_mod(a, r, p)
        e = hash(M + str(x))
        y = (r + s * e) % q
    return e, y


def verify(M, sig, pubKeyParam, v):
    """
    签名验证函数
    :param M: 消息
    :param v: 公钥
    :param pubKeyParam: 全局公钥参数
    :param sig: 签名
    :return: 验证结果
    """
    e, y = sig[0], sig[1]
    a, p, q = pubKeyParam[0], pubKeyParam[1], pubKeyParam[2]
    x = (fast_pow_mod(a, y, p) * fast_pow_mod(v, e, p)) % p

    if e == hash(M + str(x)):
        return True
    else:
        return False


def testSchnorr():
    """
    Schnorr测试函数
    :return:
    """

    # p = getBigPrime(1024)
    # q = getBigPrime(160)
    # cnt = 0
    # while (p - 1) % q != 0:
    #     q = getBigPrime(160)
    #     cnt += 1
    #     if cnt == 10000:
    #         p = getBigPrime(1024)
    #         cnt = 0
    # print("1024位大质数p = {0}\n160位大质数q = {1}".format(p, q))
    # a = 2  # a^q mod p = 1
    msg = "基于Schnorr的数字签名"
    p = 6233588875466341566113630330275552873486878881674315000002391717203321165179184214016765668971399206470119049322960064240805978144781601456277748229517456259470647256047322405573206363800989129316236832607243718624184346100338941861715113988130251202574293338708575332978108008918240726077115306442121
    q = 903569344808636464092554330241160515973915296479
    a = 1790280416633283691024656667553831515509379601966536379609622193784265347750992685294786283074032431990483382660794741449452697905240380032247426972245376314961319619940551686559535555710850888797350763947257978363297675331290475120987389290807548518382474677239002809417088237196403049028357341663344

    puKeyParam = (a, p, q)  # 全局公钥参数
    prKey, puKey = generateKey(p, q, a)

    Sig = sign(msg, prKey, puKeyParam)
    print("e:", hex(Sig[0]))
    print("y:", hex(Sig[1]))

    print("----------------")
    vRes = verify(msg, Sig, puKeyParam, puKey)
    if vRes:
        print("签名验证成功！")
    else:
        print("签名验证失败！")


if __name__ == "__main__":
    testSchnorr()