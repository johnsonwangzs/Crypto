import ECC_calculator
import fast_Pow_Mod
import math
import random


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
        y = fast_Pow_Mod.fast_pow_mod(g, u + 1, p)
        z = pow(y, 2, p)
        if z == g:
            return y
        else:
            return -1
    elif p % 8 == 5:
        u = p // 8
        z = fast_Pow_Mod.fast_pow_mod(g, 2 * u + 1, p)
        if z % p == 1:
            y = fast_Pow_Mod.fast_pow_mod(g, u + 1, p)
            return y
        elif z % p == -1 or z % p == p - 1:
            y = (2 * g * fast_Pow_Mod.fast_pow_mod(4 * g, u, p)) % p
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
            P = ECC_calculator.Point()
            P.x, P.y = xp, yp
            return P

    # 若字节串为未压缩的表示形式，PC=0x04
    # if S[0] == 4:
    #     if len(S) % 2 != 1:
    #         print("The message is a bad input!")
    #     else:  # 字节串的表示形式为PC||X1||Y1
    #         X1, Y1 = [], []
    #         for i in range(1, (len(S) - 1) // 2 + 1):
    #             X1.append(S[i])
    #         for i in range((len(S) - 1) // 2 + 1, len(S)):
    #             Y1.append(S[i])
    #
    #         # 将字节串X1转为域元素xp
    #         xp = bytes2GF(q, X1, (len(S) - 1) // 2)
    #         yp = bytes2GF(q, Y1, (len(S) - 1) // 2)
    #         print("xp:", xp)
    #         print("yp:", yp)
    #
    #         # 验证
    #         tmp1 = (yp * yp) % q
    #         tmp2 = (xp * xp * xp + a * xp + b) % q
    #         if tmp1 != tmp2:
    #             print("消息编码-字节串转点：方程验证错误！")
    #         else:
    #             P = ECC_calculator.Point()
    #             P.x, P.y = xp, yp
    #             return P


def point2Bytes(q, a, b, P):  # 4.2.9
    """
    点到字节串的转换
    :param q: 椭圆曲线参数q
    :param a: 椭圆曲线参数a
    :param b: 椭圆曲线参数b
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
    S = (PC << (cnt * 8)) + X1

    return S


def test_bytes2Point():
    # fin = open("testin", "rb")
    # S = fin.read()
    S = b'\x0212345678901234567890123456789012'
    q = 0x8542D69E_4C044F18_E8B92435_BF6FF7DE_45728391_5C45517D_722EDB8B_08F1DFC3
    a = 0x787968B4_FA32C3FD_2417842E_73BBFEFF_2F3C848B_6831D7E0_EC65228B_3937E498
    b = 0x63E4C6D3_B23B0C84_9CF84241_484BFE48_F61D59A5_B16BA06E_6E12D1DA_27C5249A
    l = math.ceil(math.log(q, 2) / 8)
    print("NOTICE: 输入字节串S的长度l（不含单字节标识符PC）须为：{0}字节".format(l))
    print("待编码消息S：", S)
    P = bytes2Point(q, a, b, S)
    print("字节串S转曲线上点P成功！")
    print("Px={0}\nPy={1}".format(hex(P.x), hex(P.y)))
    S = point2Bytes(q, a, b, P)
    print("由P还原字节串S成功！")
    print("消息S是：", S.to_bytes(l + 1, byteorder='big'))


if __name__ == "__main__":
    test_bytes2Point()
