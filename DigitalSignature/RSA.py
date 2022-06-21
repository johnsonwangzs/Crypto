import extended_GCD
import Miller_Rabin
from Power_module_FAST import *
import GCD
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
    print("公钥pk =", e)
    p = getBigPrime()
    q = getBigPrime()
    while GCD.gcd(e, (p-1)*(q-1)) != 1:  # (p-1)(q-1)需与e互质
        p = getBigPrime()
        q = getBigPrime()
    print("大素数p =", p)
    print("大素数q =", q)
    N = p * q
    print("模数N = p*q =", N)
    tmp1, tmp, tmp2 = extended_GCD.extended_gcd(e, (p - 1) * (q - 1))  # 扩展欧几里得求乘法逆元
    if tmp < 0:  # 防止使用扩展欧几里得算出的解密指数d为负数
        tmp = tmp + (p - 1) * (q - 1)
    d = tmp
    print("私钥sk =", d)
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
    m1 = fast_powMod.fast_pow_mod(ciphertext, sk % (p - 1), p)
    m2 = fast_powMod.fast_pow_mod(ciphertext, sk % (q - 1), q)
    tmp1, q_inv, tmp2 = extended_GCD.extended_gcd(q, p)
    tmp1, p_inv, tmp2 = extended_GCD.extended_gcd(p, q)
    plaintext = ((m1 * q * q_inv % N) + (m2 * p * p_inv % N)) % N
    return plaintext


def test():
    """
    测试函数
    :return: 测试结果
    """
    # graphviz = GraphvizOutput()
    # graphviz.output_file = 'RSA.png'
    # with PyCallGraph(output=graphviz):
    plaintext = 123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
    print("明文：", plaintext)
    p, q, N, pk, sk = key_generation()
    ciphertext = RSA_encrypt(plaintext, pk, N)
    print("加密完成！密文是：", ciphertext)
    print("解密完成！明文是：", RSA_decrypt(ciphertext, sk, p, q))


if __name__ == '__main__':
    # mode = eval(input("请输入模式：\n(生成密钥=0 加密=1 解密=2)"))
    # if mode == 0:
    #     p, q, N, pk, sk = key_generation()
    #     # print("大质数p={0}\n大质数q={1}\n模数N=pq={2}\n公钥pk={3}\n私钥sk={4}".format(p, q, N, pk, sk))
    # elif mode == 1:
    #     plaintext = eval(input("请输入待加密明文："))
    #     pk = eval(input("请输入公钥pk："))
    #     N = eval(input("请输入公开的模数N=p*q："))
    #     ciphertext = RSA_encrypt(plaintext, pk, N)
    #     print("加密完成！密文是：", ciphertext)
    # elif mode == 2:
    #     ciphertext = eval(input("请输入待解密密文："))
    #     sk = eval(input("请输入私钥sk："))
    #     p = eval(input("请输入大质数p："))
    #     q = eval(input("请输入大质数q："))
    #     # N = eval(input("请输入N=p*q："))
    #     plaintext = RSA_decrypt(ciphertext, sk, p, q)
    #     print("解密完成！明文是：", plaintext)

    test()
