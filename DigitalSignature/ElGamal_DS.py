import random
from Power_module_FAST import *
from GCD import *
from extended_GCD import *
from hashlib import sha1
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def generateKey(p, g):
    """
    密钥生成函数，生成加解密时所需要的的公私钥
    :param p: 质数
    :param g: p的一个原根
    :return: 加解密时所需要的的公私钥
    """
    d = random.randint(2, p - 2)
    e = fast_pow_mod(g, d, p)
    return d, e


def sign(g, d, pt, p):
    """
    签名函数
    :param g: 原根
    :param p: 质数
    :param d: 用户私钥
    :param pt: 明文
    :return: 签名结果sig
    """
    h = hash(pt) % p
    if h >= p:  # 0 <= h <= p-1
        print("bad input: plaintext")
        return

    k = random.randint(1, p - 1)
    while gcd(k, p - 1) != 1:
        k = random.randint(1, p - 1)

    S1 = fast_pow_mod(g, k, p)

    kInv = extended_gcd(k, p - 1)[1]

    S2 = kInv * (h - d * S1) % (p - 1)

    return S1, S2


def verify(e, g, p, sig, pt):
    """
    签名验证函数
    :param e: 公钥
    :param g: 原根
    :param p: 质数
    :param sig: 签名(S1, S2)
    :param pt: 消息（明文）
    :return: 签名结果
    """
    h = hash(pt) % p

    S1, S2 = sig[0], sig[1]

    V1 = fast_pow_mod(g, h, p)

    V2 = (fast_pow_mod(e, S1, p) * fast_pow_mod(S1, S2, p)) % p

    if V1 == V2:
        return True
    else:
        return False


def testElGamal():
    """
    ElGamal数字签名算法测试函数
    :return:
    """
    # q = eval(input("输入质数p："))
    # a = eval(input("输入原根g："))
    # m = input("输入消息M：")
    q = 1909858912667014946213159569319
    a = 92179309246465225943487
    m = "基于ElGamal的数字签名"

    # 签名
    Xa, Ya = generateKey(q, a)
    print("私钥：{0}\n公钥：{1}".format(Xa, Ya))
    Sig = sign(a, Xa, m, q)
    print("签名：\nS1={0}\nS2={1}".format(Sig[0], Sig[1]))

    """
    模拟签名被更改：
    Sig[0] = ?
    Sig[1] = ?
    """

    print("----------------")
    # 验签
    vRes = verify(Ya, a, q, Sig, m)
    if vRes:
        print("签名验证成功！")
    else:
        print("签名验证失败！")


if __name__ == "__main__":
    testElGamal()
