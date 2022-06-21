from function import extended_GCD
from function import Miller_Rabin
from function.Power_module_FAST import *
from function import GCD
from random import randint


def getBigPrime():
    """
    取得大质数
    :return:一个1024以上二进制位的大质数
    """
    rnd = 0
    for i in range(32):  # 1024个二进制位
        rnd = rnd * 65536 + randint(0, 65536)  # 以16个二进制位为一组，共生成512位
    rnd = rnd | (1 << 511)  # 保证至少为512二进制位
    rnd = rnd | 1  # 保证为奇数

    while True:
        if Miller_Rabin.miller_rabin_api(rnd, 10):
            return rnd
        rnd += 2


def key_generation():
    """
    生成公钥和私钥
    :return: N=p*q，解密指数d
    """
    print("Calculating (p, q, N, pk, sk)......Please wait!")
    e = getBigPrime()
    p = getBigPrime()
    q = getBigPrime()
    while GCD.gcd(e, (p-1)*(q-1)) != 1:  # (p-1)(q-1)需与e互质
        p = getBigPrime()
        q = getBigPrime()
    N = p * q
    tmp1, tmp, tmp2 = extended_GCD.extended_gcd(e, (p - 1) * (q - 1))  # 扩展欧几里得求乘法逆元
    if tmp < 0:  # 防止使用扩展欧几里得算出的解密指数d为负数
        tmp = tmp + (p - 1) * (q - 1)
    d = tmp
    return p, q, N, e, d


def RSA_encrypt(plaintext, pk, N):
    """
    RSA加密算法
    :param plaintext: 待加密明文
    :param pk: 公钥
    :param N: 模数N=p*q
    :return: 密文
    """
    ciphertext = fast_pow_mod(plaintext, pk, N)
    return ciphertext


def RSA_decrypt(ciphertext, sk, p, q):
    """
    RSA解密算法
    :param ciphertext: 待解密密文
    :param sk: 私钥
    :param p: 大质数p
    :param q: 大质数q
    :return: 明文
    """
    N = p * q
    # plaintext = fast_powMod.fast_pow_mod(ciphertext, sk, N)
    # 使用CRT加速解密过程
    m1 = fast_pow_mod(ciphertext, sk % (p - 1), p)
    m2 = fast_pow_mod(ciphertext, sk % (q - 1), q)
    tmp1, q_inv, tmp2 = extended_GCD.extended_gcd(q, p)
    tmp1, p_inv, tmp2 = extended_GCD.extended_gcd(p, q)
    plaintext = ((m1 * q * q_inv % N) + (m2 * p * p_inv % N)) % N
    return plaintext
