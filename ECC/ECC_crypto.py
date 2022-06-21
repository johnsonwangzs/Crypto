from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import ECC_calculator as ECC_cal
import MessageEncoding as MesEnc
import random


def gen_pk(q, a, G, n, nb):
    """
    根据用户B（接收方）的私钥产生公钥
    :param nb: 用户B的私钥
    :param n: 基点G的阶n
    :param gx: 基点G的x坐标
    :param gy: 基点G的y坐标
    :return: B的公钥pb
    """
    if nb >= n:
        print("接收方的私钥不合法！")
        return

    Pb = ECC_cal.fast_multiply(G, nb, q, a)

    return Pb


def ECC_encryption(q, a, b, gx, gy, n, nb, S):
    """
    ECC加密算法
    :param P: 待加密的消息（已编码为点）
    :param q: 椭圆曲线参数q
    :param a: 椭圆曲线参数a
    :param b: 椭圆曲线参数b
    :param gx: 基点G的x坐标
    :param gy: 基点G的y坐标
    :param n: 基点G的阶n
    :param nb: 用户B的私钥nb
    :return: 密文C
    """
    G = ECC_cal.Point()
    G.x, G.y = gx, gy

    Pk = gen_pk(q, a, G, n, nb)  # 用户A（发送方）获取用户B（接收方）的公钥
    print("公钥的x坐标是：", hex(Pk.x))
    print("公钥的y坐标是：", hex(Pk.y))
    print("----公钥生成：成功！----")

    P = MesEnc.bytes2Point(q, a, b, S)  # A将待加密消息编码为椭圆上的一个点
    print("----消息编码：输入字节消息串S-->曲线上点P：成功！----")

    k = random.randint(0, n - 1)
    C1 = ECC_cal.fast_multiply(G, k, q, a)
    C2 = ECC_cal.add(P, ECC_cal.fast_multiply(Pk, k, q, a), q, a)
    print("----加密：成功！----")

    print("C1的x坐标是：", hex(C1.x))
    print("C1的y坐标是：", hex(C1.y))
    print("C2的x坐标是：", hex(C2.x))
    print("C2的y坐标是：", hex(C2.y))
    return C1, C2


def ECC_decryption(q, a, b, gx, gy, n, nb, C1_x, C1_y, C2_x, C2_y):
    """
    ECC解密算法
    :param q: 椭圆曲线参数q
    :param a: 椭圆曲线参数a
    :param b: 椭圆曲线参数b
    :param gx: 基点G的x坐标
    :param gy: 基点G的y坐标
    :param n: 基点G的阶n
    :param nb: 用户B的私钥nb
    :param C1_x: 密文C1的x坐标
    :param C1_y: 密文C1的y坐标
    :param C2_x: 密文C2的x坐标
    :param C2_y: 密文C2的y坐标
    :return: 明文字节串m
    """
    C1 = ECC_cal.Point()
    C2 = ECC_cal.Point()
    G = ECC_cal.Point()
    C1.x, C1.y = C1_x, C1_y
    C2.x, C2.y = C2_x, C2_y
    G.x, G.y = gx, gy

    P = ECC_cal.add(C2, ECC_cal.neg_P(ECC_cal.fast_multiply(C1, nb, q, a), q), q, a)
    print("----解密：成功！----")

    m = MesEnc.point2Bytes(q, a, b, P)  # B将椭圆上的一个点还原为明文字节串
    print("----还原明文字节串：成功！----")

    tmp, cnt = m, 0  # 求m的字节串长度
    while tmp > 0:
        tmp = tmp >> 8
        cnt += 1
    print("解得明文是：", m.to_bytes(cnt, byteorder='big'))
    return m


def test_crypto():
    """
    测试函数
    :return:
    """
    fin = open("testin", "rb")
    S = fin.read()

    # P = ECC_cal.Point()
    # P.x = 0x435B39CC_A8F3B508_C1488AFC_67BE491A_0F7BA07E_581A0E48_49A5CF70_628A7E0A
    # P.y = 0x75DDBA78_F15FEECB_4C7895E2_C1CDF5FE_01DEBB2C_DBADF45399CCF77B_BA076A42
    q = 0x8542D69E_4C044F18_E8B92435_BF6FF7DE_45728391_5C45517D_722EDB8B_08F1DFC3
    a = 0x787968B4_FA32C3FD_2417842E_73BBFEFF_2F3C848B_6831D7E0_EC65228B_3937E498
    b = 0x63E4C6D3_B23B0C84_9CF84241_484BFE48_F61D59A5_B16BA06E_6E12D1DA_27C5249A
    n = 0x8542D69E_4C044F18_E8B92435_BF6FF7DD_29772063_0485628D_5AE74EE7_C32E79B7
    gx = 0x435B39CC_A8F3B508_C1488AFC_67BE491A_0F7BA07E_581A0E48_49A5CF70_628A7E0A
    gy = 0x75DDBA78_F15FEECB_4C7895E2_C1CDF5FE_01DEBB2C_DBADF453_99CCF77B_BA076A42
    nb = 0x1649AB77_A00637BD_5E2EFE28_3FBF3535_34AA7F7C_B89463F2_08DDBC29_20BB0DA0
    print("要加密的明文是：", S)

    # 加密
    C1, C2 = ECC_encryption(q, a, b, gx, gy, n, nb, S)

    # 解密
    m = ECC_decryption(q, a, b, gx, gy, n, nb, C1.x, C1.y, C2.x, C2.y)


if __name__ == "__main__":
    # mode = eval(input("请输入加解密模式。mode=0-->加密。mode=1-->解密。"))
    # if mode == 0:
    #     fin = open("testin", "rb")
    #     S = fin.read()
    #     q = eval(input("请输入椭圆曲线参数q："))
    #     a = eval(input("请输入椭圆曲线参数a："))
    #     b = eval(input("请输入椭圆曲线参数b："))
    #     gx = eval(input("请输入基点G的x坐标："))
    #     gy = eval(input("请输入基点G的y坐标："))
    #     n = eval(input("请输入基点G的阶n："))
    #     nb = eval(input("请输入用户B（接收方）的私钥nb："))
    #     C1, C2 = ECC_encryption(S, q, a, b, gx, gy, n, nb)
    # elif mode == 1:
    #     q = eval(input("请输入椭圆曲线参数q："))
    #     a = eval(input("请输入椭圆曲线参数a："))
    #     b = eval(input("请输入椭圆曲线参数b："))
    #     gx = eval(input("请输入基点G的x坐标："))
    #     gy = eval(input("请输入基点G的y坐标："))
    #     n = eval(input("请输入基点G的阶n："))
    #     nb = eval(input("请输入用户B（接收方）的私钥nb："))
    #     C1_x = eval(input("请输入密文C1的x坐标："))
    #     C1_y = eval(input("请输入密文C1的y坐标："))
    #     C2_x = eval(input("请输入密文C2的x坐标："))
    #     C2_y = eval(input("请输入密文C2的y坐标："))
    #     M = ECC_decryption(q, a, b, gx, gy, n, nb, C1_x, C1_y, C2_x, C2_y)
    test_crypto()