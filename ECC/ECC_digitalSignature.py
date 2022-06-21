import ECC_crypto
import ECC_calculator as ECC_cal
import sm3
import math
import random
import extended_GCD as exGCD
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def int2Bytes(x, l):  # 4.2.2
    """
    整数到字节串的转换
    :param x: 非负整数x
    :param l: 需转成的字节串的长度
    :return: 列表存储的字节串s（按从高位到低位顺序）
    """
    s = []
    tmp, cnt = x, 0
    while tmp > 0:
        tmp = tmp >> 8
        cnt += 1
    if cnt < l:  # 若转换后的字节串不够l位，补0凑齐
        for i in range(l - cnt):
            s.append(0)
    for i in range(cnt):
        s.append(x >> (8 * (cnt - 1 - i)) & 0xFF)
    return s


def GFEle2Bytes(q, alpha):  # 4.2.6
    """
    域元素到字节串的转换
    :param q: 椭圆参数
    :param alpha: 域元素
    :return: 字节串S（按从高位到低位存储在列表）
    """
    t = math.ceil(math.log(q, 2))
    l = math.ceil(t / 8)
    S = int2Bytes(alpha, l)
    return S


def bytes2Bit(M):  # 4.2.5
    """
    字节串到比特串的转换
    :param M: 字节串
    :return: 比特串
    """
    B = []
    for i in range(len(M)):
        for j in range(8):
            B.append((M[i] >> (7 - j)) & 0b1)
    return B


def GFEle2Bit(q, alpha):
    """
    域元素转比特串
    :param q: 椭圆参数
    :param alpha: 域元素
    :return: 比特串
    """
    res1 = GFEle2Bytes(q, alpha)
    res2 = bytes2Bit(res1)
    return res2


def bit2Int_type1(bitList):
    """
    比特串转整数（列表中为int型的0/1）
    :param bitList: 比特串
    :return: 整数
    """
    res = 0
    for num in bitList:
        res = (res << 1) + num
    return res


def bit2Int_type2(bitList):
    """
    比特串转整数
    :param bitList: 比特串（列表中为字符类型的'0'/'1'）
    :return: 整数
    """
    res = 0
    for num in bitList:
        res = (res << 1) + ord(num) - 48
    return res


def cal_Za(p, G, Pa, a, b, ID_a, ENTL_a):
    """
    计算Za
    :param p: 椭圆参数
    :param G: 基点G
    :param Pa: A的公钥
    :param a: 椭圆参数
    :param b: 椭圆参数
    :param ID_a: 用户A的ID
    :param ENTL_a: ID_a的比特长度
    :return: Za
    """
    # 转为比特串并连接——ENTL_a + ID_a + a + b + gx + gy + ax + ay
    afterBitAttach = GFEle2Bit(p, ENTL_a) + GFEle2Bit(p, ID_a) + GFEle2Bit(p, a) + GFEle2Bit(p, b) \
        + GFEle2Bit(p, G.x) + GFEle2Bit(p, G.y) + GFEle2Bit(p, Pa.x) + GFEle2Bit(p, Pa.y)

    # 转为整数，然后调用杂凑算法
    afterBitAttach_2int = bit2Int_type1(afterBitAttach)
    # Za = bit2Int_type2(sm3.IterFunction(sm3.fillFunction(afterBitAttach_2int)))
    Za = hash(afterBitAttach_2int)
    print("Za =", hex(Za))
    return Za


def digitalSignature_snd(p, a, b, gx, gy, n, da, ID_a, ENTL_a, M):
    """
    发送方——数字签名的生成算法
    :param p: 椭圆参数
    :param a: 椭圆参数
    :param b: 椭圆参数
    :param gx: 基点G的x坐标
    :param gy: 基点G的y坐标
    :param n: 基点G的阶
    :param da: A的私钥
    :param ID_a: 用户A的ID
    :param ENTL_a: ID_a的比特长度
    :param M: 待发送消息
    :return: 消息M的数字签名(r,s)，A的公钥
    """
    print("--------SENDER--------")
    print("M =", hex(M))

    # 基点G
    G = ECC_cal.Point()
    G.x, G.y = gx, gy

    # 求A的公钥
    Pa = ECC_crypto.gen_pk(p, a, G, n, da)

    # 计算Za
    Za = cal_Za(p, G, Pa, a, b, ID_a, ENTL_a)

    # step A1
    tmp, cnt = M, 0
    while tmp > 0:
        tmp = tmp >> 8
        cnt += 1
    M1 = (Za << (cnt * 8)) + M

    # step A2
    # e = bit2Int_type2(sm3.IterFunction(sm3.fillFunction(M1)))
    e = hash(M1)

    r, s = 0, 0
    while True:
        # step A3
        k = random.randint(1, n - 1)
        # k = 0x6CB28D99_385C175C_94F94E93_4817663F_C176D925_DD72B727_260DBAAE_1FB2F96F

        # step A4
        X1 = ECC_cal.fast_multiply(G, k, p, a)
        x1 = X1.x

        # step A5
        r = (e + x1) % n
        if r == 0 or (r + k == n):
            continue

        # step A6
        s = (exGCD.extended_gcd(1 + da, n)[1] * (k - r * da)) % n
        if s == 0:
            continue
        break

    # step A7
    print("snd: (r, s)")
    print("r =", hex(r))
    print("s =", hex(s))
    return r, s, Pa


def digitalSignature_rcv(M, r, s, p, n, gx, gy, Pa, a, b, ID_a, ENTL_a):
    """
    接收方——数字签名校验
    :param M: B收到的消息
    :param r: A发送的签名信息r
    :param s: A发送的签名消息s
    :param p: 椭圆参数
    :param n: 基点G的阶
    :param gx: 基点G的x坐标
    :param gy: 基点G的y坐标
    :param Pa: A的公钥
    :param a: 椭圆参数
    :param b: 椭圆参数
    :param ID_a: 用户A的ID
    :param ENTL_a: ID_a的比特长度
    :return:
    """
    print("--------RECEIVER--------")
    print("M' =", hex(M))
    print("rcv: (r', s')")
    print("r' =", hex(r))
    print("s' =", hex(s))

    G = ECC_cal.Point()
    G.x, G.y = gx, gy

    Za = cal_Za(p, G, Pa, a, b, ID_a, ENTL_a)

    # step B1
    if r < 1 or r > n - 1:
        print("--------\nRes: Error! B1：r校验出错！")
        return False

    # step B2
    if s < 1 or s > n - 1:
        print("--------\nRes: Error! B2：s校验出错！")
        return False

    # step B3
    tmp, cnt = M, 0
    while tmp > 0:
        tmp = tmp >> 8
        cnt += 1
    M1 = (Za << (cnt * 8)) + M

    # step B4
    # e = bit2Int_type2(sm3.IterFunction(sm3.fillFunction(M1)))
    e = hash(M1)

    # step B5
    t = (r + s) % n
    if t == 0:
        print("--------\nRes: Error! B5：t校验出错！")
        return False

    # step B6
    X1 = ECC_cal.add(ECC_cal.fast_multiply(G, s, p, a), ECC_cal.fast_multiply(Pa, t, p, a), p, a)

    # step B7
    R = (e + X1.x) % n
    if R == r:
        print("--------\nRes: Congratulation! 校验通过！")
        return True
    else:
        print("--------\nRes: Error! B7：R校验出错！")
        return False


def testDS():
    p = 0x8542D69E_4C044F18_E8B92435_BF6FF7DE_45728391_5C45517D_722EDB8B_08F1DFC3
    a = 0x787968B4_FA32C3FD_2417842E_73BBFEFF_2F3C848B_6831D7E0_EC65228B_3937E498
    b = 0x63E4C6D3_B23B0C84_9CF84241_484BFE48_F61D59A5_B16BA06E_6E12D1DA_27C5249A
    gx = 0x421DEBD6_1B62EAB6_746434EB_C3CC315E_32220B3B_ADD50BDC_4C4E6C14_7FEDD43D
    gy = 0x0680512B_CBB42C07_D47349D2_153B70C4_E5D7FDFC_BFA36EA1_A85841B9_E46E09A2
    da = 0x128B2FA8_BD433C6C_068C8D80_3DFF7979_2A519A55_171B1B65_0C23661D_15897263
    n = 0x8542D69E_4C044F18_E8B92435_BF6FF7DD_29772063_0485628D_5AE74EE7_C32E79B7
    ID_a = 0x414C_49434531_32334059_41484F4F_2E434F4D  # ALICE123@YAHOO,COM
    ENTL_a = 0x0090
    M = 0x6D657373_61676520_64696765_7374  # "message digest"
    # Za = 0xF4A38489_E32B45B6_F876E3AC_2168CA39_2362DC8F_23459C1D_1146FC3D_BFB7BC9A
    # M = 0x6D657373_61676520_64696765_7374
    r, s, Pa = digitalSignature_snd(p, a, b, gx, gy, n, da, ID_a, ENTL_a, M)

    digitalSignature_rcv(M, r, s, p, n, gx, gy, Pa, a, b, ID_a, ENTL_a)


if __name__ == "__main__":
    # print("请输入椭圆曲线系统参数（均为16进制）")
    # q = eval(input("请输入椭圆曲线参数q："))
    # a = eval(input("请输入椭圆曲线参数a："))
    # b = eval(input("请输入椭圆曲线参数b："))
    # gx = eval(input("请输入基点G的x坐标："))
    # gy = eval(input("请输入基点G的y坐标："))
    # n = eval(input("请输入基点G的阶n："))
    # da = eval(input("请输入用户A的私钥："))
    # ID_a = eval(input("请输入用户A的身份ID_A："))
    # ENTL_a = eval(input("请输入ID_A的比特长度（2字节）："))

    # digitalSignature(p, a, b, gx, gy, n, da, ID_a, ENTL_a)

    testDS()
