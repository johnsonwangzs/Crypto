from ECC_calculator import *
from random import *
import math
from SHA1 import *
from Power_module_FAST import *
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

v = 160  # SHA-1函数的hash值


def gen_pk(q, a, G, n, nb):
    """
    根据用户B（接收方）的私钥产生公钥
    :param G: 基点G
    :param a: 椭圆参数
    :param q: 椭圆参数
    :param nb: 用户B的私钥
    :param n: 基点G的阶n
    :return: B的公钥pb
    """
    if nb >= n:
        print("接收方的私钥不合法！")
        return
    Pb = fast_multiply(G, nb, q, a)
    return Pb


def Lucas(p, X, Y, k):
    """
    Lucas序列的计算
    :param p: 奇素数p
    :param X: 整数X
    :param Y: 整数Y
    :param k: 正整数k
    :return: X和Y的Lucas序列Uk modp，Vk modp
    """
    delta = X * X - 4 * Y

    # 计算k的二进制表示
    k_bin = []
    while k > 0:
        k_bin.append(k & 0b1)
        k = k >> 1
    r = len(k_bin) - 1

    U, V = 1, X
    for i in range(r - 1, -1, -1):
        U = (U * V) % p
        V = ((V * V + delta * U * U) / 2) % p
        if k_bin[i] == 1:
            U = ((X * U + V) / 2) % p
            V = ((X * V + delta * U) / 2) % p
    return U, V


def cal_squareRoot(g, p):
    """
    模素数平方根的求解
    :param g: 整数g
    :param p: 奇素数p（模数）
    :return: 若存在g的平方根，则输出一个平方根modp，否则输出-1
    """
    if p % 4 == 3:
        u = p // 4
        y = fast_pow_mod(g, u + 1, p)
        z = pow(y, 2, p)
        if z == g:
            return y
        else:
            return -1
    elif p % 8 == 5:
        u = p // 8
        z = fast_pow_mod(g, 2 * u + 1, p)
        if z % p == 1:
            y = fast_pow_mod(g, u + 1, p)
            return y
        elif z % p == -1 or z % p == p - 1:
            y = (2 * g * fast_pow_mod(4 * g, u, p)) % p
            return y
        else:
            return -1
    elif p % 8 == 1:
        u = p // 8
        Y = g
        while True:
            X = random.randint(1, p - 1)
            # 计算Lucas序列元素
            U, V = Lucas(p, X, Y, 4 * u + 1)
            if V * V % p == 4 * Y:
                y = (V / 2) % p
                return y
            if U % p != 1 and U % p != p - 1:
                return -1


def restore_yp(q, a, b, xp, yp_hat):  # 附录A.5
    """
    Fq上椭圆曲线点的解压缩，由yp_hat得到yp
    :param q: 定义曲线的参数
    :param a: 定义曲线的参数
    :param b: 定义曲线的参数
    :param xp: P=(xp,yp)是定义在Fq上椭圆曲线E上的一个点
    :param yp_hat: 是yp最右边的一个比特
    :return: 解压缩后得到的yp
    """
    alpha = (pow(xp, 3) + a * xp + b) % q
    beta = cal_squareRoot(alpha % q, q)
    if beta == -1:
        print("不存在平方根！")
    if beta & 0b1 == yp_hat:
        yp = beta
    else:
        yp = q - beta
    return yp


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


def bytes2Integer(S, k):  # 4.2.3
    """
    字节串到整数的转换
    :param S: 字节串
    :param k: 字节串长度
    :return: 一个整数
    """
    x = 0
    for i in range(k - 1, -1, -1):
        x += pow(2, 8 * i) * S[k - 1 - i]
    return x


def bit2Int(bitList):  # 4.2.4
    """
    比特串转整数（列表中为int型的0/1）
    :param bitList: 比特串
    :return: 整数
    """
    res = 0
    for num in bitList:
        res = (res << 1) + num
    return res


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


def bytes2GF(q, S, k):  # 4.2.7
    """
    Fq中q为奇素数时，字节串到域元素的转换
    :param q: 椭圆曲线参数
    :param S: 字节串
    :param k: 字节串长度
    :return: 域元素
    """
    integerRes = bytes2Integer(S, k)
    if 0 <= integerRes <= q - 1:
        return integerRes
    else:
        print("消息编码-字节串转域元素：发生错误！")
        return


def point2Bytes(q, P):  # 4.2.9
    """
    点到字节串的转换
    :param q: 椭圆曲线参数q
    :param P: 输入的点
    :return: 将点还原为字节串
    """
    # 选用压缩的表示形式
    xp, yp = P.x, P.y

    # 将xp转成长度l的字节串X1
    l = math.ceil(math.log(q, 2) / 8)
    X1 = xp

    # 计算比特yp_hat，其是yp最右边的一个比特
    PC = 0
    yp_hat = yp & 0b1
    if yp_hat == 0:
        PC = 0x02
    elif yp_hat == 1:
        PC = 0x03

    # 字节串S=PC||X1
    tmp, cnt = X1, 0
    while tmp > 0:
        tmp = tmp >> 8
        cnt += 1
    S = ((PC << (cnt * 8)) + X1).to_bytes(l + 1, byteorder='big')

    return S


def bytes2Point(q, a, b, S):  # 4.2.10
    """
    字节串到点的转换
    :param q: 椭圆曲线参数q
    :param a: 椭圆曲线参数a
    :param b: 椭圆曲线参数b
    :param S: 输入的消息（字节串形式）
    :return: 将消息编码形成的一个点
    """
    # 若字节串为压缩的表示形式，PC=0x02或0x03
    if S[0] == 2 or S[0] == 3:

        X1 = []
        for byte in S:  # 字节串的表示形式为PC||X
            X1.append(byte)

        # 检测待编码消息长度
        l = math.ceil(math.log(q, 2) / 8)
        if len(X1) - 1 != l:
            print("待编码消息S的长度不符合规范！"
                  "长度应为{0}字节，且第一个字节为标识符PC！".format(l + 1))
            return

        # 将字节串X1转为域元素xp
        xp = bytes2GF(q, X1[1:], len(S) - 1)

        # 将(xp, yp)转换为椭圆曲线上的一个点
        yp_tmp = 0
        if S[0] == 2:
            yp_tmp = 0
        elif S[0] == 3:
            yp_tmp = 1
        yp = restore_yp(q, a, b, xp, yp_tmp)

        # 验证
        tmp1 = (yp * yp) % q
        tmp2 = (xp * xp * xp + a * xp + b) % q
        if tmp1 != tmp2:
            print("消息编码-字节串转点：方程验证错误！")
        else:
            P = Point()
            P.x, P.y = xp, yp
            return P

    # 若字节串为未压缩的表示形式，PC=0x04
    if S[0] == 4:
        if len(S) % 2 != 1:
            print("The message is a bad input!")
        else:  # 字节串的表示形式为PC||X1||Y1
            X1, Y1 = [], []
            for i in range(1, (len(S) - 1) // 2 + 1):
                X1.append(S[i])
            for i in range((len(S) - 1) // 2 + 1, len(S)):
                Y1.append(S[i])

            # 将字节串X1转为域元素xp
            xp = bytes2GF(q, X1, (len(S) - 1) // 2)
            yp = bytes2GF(q, Y1, (len(S) - 1) // 2)
            print("xp:", xp)
            print("yp:", yp)

            # 验证
            tmp1 = (yp * yp) % q
            tmp2 = (xp * xp * xp + a * xp + b) % q
            if tmp1 != tmp2:
                print("消息编码-字节串转点：方程验证错误！")
            else:
                P = Point()
                P.x, P.y = xp, yp
                return P


def KDF(Z, klen):
    """
    密钥派生函数
    :param Z: 比特串
    :param klen: 整数klen
    :return: 长度为klen的密钥数据比特串K
    """
    global v
    ct = 0  # 32bit计数器

    Ha = [0]
    for i in range(1, math.ceil(klen / v) + 1):
        Ha_i = SHA1(bit2Int(Z).to_bytes(math.ceil(len(Z) / 8), byteorder='big') + ct.to_bytes(4, byteorder='big'))
        Ha.append(Ha_i)
        ct += 1
    if klen % v == 0:
        Ha_last = bytes2Bit(int2Bytes(Ha[math.ceil(klen / v)], 20))
    else:
        Ha_last = bytes2Bit(int2Bytes(Ha[math.ceil(klen / v)], 20))[:klen - v * math.floor(klen / v)]
    K = []
    for i in range(1, math.ceil(klen / v)):
        K = K + bytes2Bit(int2Bytes(Ha[i], 20))
    K = K + Ha_last
    return K


def encrypt(M, n, q, a, G, Pb):
    """
    SM2公钥加密-加密算法
    :param G: 基点
    :param a: 参数
    :param q: 参数
    :param n: 基点的阶
    :param Pb: 接收方的公钥
    :param M: 输入的消息
    :return:
    """
    klen = 8 * len(M)  # 消息M的比特长度
    M_int = 0
    for i in range(0, len(M)):
        M_int = (M_int << 8) + M[i]
    M_bit = bytes2Bit(int2Bytes(M_int, len(M)))

    while True:
        k = randint(1, n - 1)  # Step-A1

        C1 = fast_multiply(G, k, q, a)  # Step-A2
        C1_bit = bytes2Bit(point2Bytes(q, C1))  # 点-->比特串

        kPb = fast_multiply(Pb, k, q, a)  # Step-A4
        x_bit = bytes2Bit(GFEle2Bytes(q, kPb.x))  # 域元素-->比特串
        y_bit = bytes2Bit(GFEle2Bytes(q, kPb.y))

        t = KDF(x_bit + y_bit, klen)  # Step-A5
        if t != [0] * klen:
            break

    C2 = []
    for i in range(klen):
        C2.append(M_bit[i] ^ t[i])  # step-A6

    tmp = bit2Int(x_bit + M_bit + y_bit)
    C3 = SHA1(tmp.to_bytes(math.ceil(len(x_bit + M_bit + y_bit) / 8), byteorder='big'))

    C = C1_bit, bytes2Bit(int2Bytes(C3, 20)), C2  # Step-A7

    return C


def decrypt(C, q, a, b, db):
    """
    SM2公钥加密-解密算法
    :param C: 密文 C1||C3||C2
    :param q: 参数
    :param a: 参数
    :param b: 参数
    :param db: 接收方的私钥
    :return:
    """
    C1, C2, C3 = C[0], C[2], C[1]
    klen = len(C2)

    C1_int = bit2Int(C1)
    C1_byte = int2Bytes(C1_int, math.ceil(len(C[0]) / 8))
    C1_point = bytes2Point(q, a, b, C1_byte)
    x1, y1 = C1_point.x, C1_point.y
    if (y1 * y1) % q != (x1 * x1 * x1 + a * x1 + b) % q:
        print("不满足椭圆方程！")  # Step-B1: 验证C1是否满足椭圆方程
        return -1

    dC1 = fast_multiply(C1_point, db, q, a)  # Step-B3
    x_bit = bytes2Bit(GFEle2Bytes(q, dC1.x))  # 域元素-->比特串
    y_bit = bytes2Bit(GFEle2Bytes(q, dC1.y))

    t = KDF(x_bit + y_bit, klen)  # Step-B4
    if t == [0] * klen:
        print("t为全0比特串！")
        return -1

    M = []  # Step-B5
    for i in range(klen):
        M.append(C2[i] ^ t[i])

    tmp = x_bit + M + y_bit
    tmp_byte = int2Bytes(bit2Int(tmp), math.ceil(len(tmp) / 8))

    u = SHA1(tmp_byte)  # Step-B6
    C3_int = bit2Int(C3)
    if C3_int != u:
        print("C3错误！")
        return -1

    M_byte = int2Bytes(bit2Int(M), math.ceil(len(M) / 8))
    res = b''
    for i in range(len(M_byte)):
        res = res + M_byte[i].to_bytes(1, byteorder='big')
    return res


def test_Crypto():
    """
    SM2公钥加密算法测试函数
    :return:
    """
    fin = open("SM2_testin", "rb")
    M = fin.read()
    # M = b'\x02abcdefghijklmnopqrstuvwxyz123456'
    q = 0x8542D69E_4C044F18_E8B92435_BF6FF7DE_45728391_5C45517D_722EDB8B_08F1DFC3
    a = 0x787968B4_FA32C3FD_2417842E_73BBFEFF_2F3C848B_6831D7E0_EC65228B_3937E498
    b = 0x63E4C6D3_B23B0C84_9CF84241_484BFE48_F61D59A5_B16BA06E_6E12D1DA_27C5249A
    n = 0x8542D69E_4C044F18_E8B92435_BF6FF7DD_29772063_0485628D_5AE74EE7_C32E79B7
    gx = 0x435B39CC_A8F3B508_C1488AFC_67BE491A_0F7BA07E_581A0E48_49A5CF70_628A7E0A
    gy = 0x75DDBA78_F15FEECB_4C7895E2_C1CDF5FE_01DEBB2C_DBADF453_99CCF77B_BA076A42
    nb = 0x1649AB77_A00637BD_5E2EFE28_3FBF3535_34AA7F7C_B89463F2_08DDBC29_20BB0DA0
    print("加密前明文是（字节串）：", M)
    G = Point()
    G.x, G.y = gx, gy
    # 【接收方】根据私钥生成公钥
    Pb = gen_pk(q, a, G, n, nb)
    # 【发送方】用公钥加密消息
    C = encrypt(M, n, q, a, G, Pb)
    print("加密后密文（比特串）：", C)
    # 【接收方】用私钥解密消息
    res = decrypt(C, q, a, b, nb)
    if res != -1:
        print("解密后明文是（字节串）：", res)
    else:
        print("解密错误！")
    return


if __name__ == "__main__":
    test_Crypto()
