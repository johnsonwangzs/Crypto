from function import ECC_calculator as ECC_cal
from function.constPara import *


def gen_pk(na, nb):
    """
    用户A和用户B根据各自的私钥生成公钥
    :param na: 用户A的私钥na
    :param nb: 用户B的私钥nb
    :return: A的公钥pa和B的公钥pb
    """
    if n < na:
        print("用户A的私钥不合法！")
        return
    if n < nb:
        print("用户B的私钥不合法！")
        return
    G = ECC_cal.Point()
    G.x, G.y = gx, gy
    Pa = ECC_cal.fast_multiply(G, na, q, a)
    Pb = ECC_cal.fast_multiply(G, nb, q, a)
    return Pa, Pb


def checkIsSuccess(keyA, keyB):
    """
    检查keyA和keyB的一致性
    :param keyA: A计算得到的公共密钥
    :param keyB: B计算得到的公共密钥
    :return: 是否一致
    """
    if keyA.x == keyB.x and keyA.y == keyB.y:
        print("公共密钥一致，交换成功！")
    else:
        print("公共密钥不一致，交换失败！")


def get_publicKey(sk, Pk):
    """
    计算公共密钥
    :param sk:一方的私钥
    :param Pk: 另一方的公钥
    :return: 公共密钥
    """
    key = ECC_cal.fast_multiply(Pk, sk, q, a)
    return key


def DH(na, nb):
    """
    基于ECC的Diffie-Hellman密钥交换协议
    :param na: 用户A的私钥na
    :param nb: 用户B的私钥nb
    :return: 无，输出交换结果
    """
    Pa, Pb = gen_pk(na, nb)
    print("A的公钥：({0},{1})".format(hex(Pa.x), hex(Pa.y)))
    print("B的公钥：({0},{1})".format(hex(Pb.x), hex(Pb.y)))
    keyA, keyB = get_publicKey(na, Pb), get_publicKey(nb, Pa)
    print("A计算得到的公共密钥：({0},{1})".format(hex(keyA.x), hex(keyA.y)))
    print("B计算得到的公共密钥：({0},{1})".format(hex(keyB.x), hex(keyB.y)))
    checkIsSuccess(keyA, keyB)
