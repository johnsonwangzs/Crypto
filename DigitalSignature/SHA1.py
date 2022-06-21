"""
SHA-1算法
"""
import copy
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def padding(M, cnt):
    """
    填充函数
    :param M: 待填充的消息
    :param cnt: 最后一个分组的原始比特长度
    :return: 填充好的分组
    """
    global N

    total = N * 512 + cnt
    if total > 0x10000000000000000:
        print("原始长度超出2^64bit范围！")
        return

    index = N
    if cnt == 512:  # 如果消息恰好完整填满最后一个分组
        N += 1
        index = N
        M.append([])
        M[index].append(1)
        for i in range(447):
            M[index].append(0)
    else:
        padNum = 448 - cnt
        M[index].append(1)
        for i in range(padNum - 1):
            M[index].append(0)

    for i in range(64):
        M[index].append((total >> (63 - i)) & 0b1)

    return M


def divide(S):
    """
    消息分组函数
    :param S: 消息（字节串）
    :return: 分组、填充好的消息
    """
    global N
    M, cnt, index = [[]], 0, 0

    for aByte in S:  # 按字节读入
        if cnt == 512:  # 每512bit作为一个分组
            index += 1
            cnt = 0
            M.append([])
        for i in range(8):
            M[index].append((aByte >> (7 - i)) & 0b1)
        cnt += 8

    N = index
    M = copy.deepcopy(padding(M, cnt))

    return M


def extend(Y):
    """
    字节扩展函数
    :param Y: 当前512bit的子消息分组
    :return: 扩展后的80*32bit
    """
    W = []

    for i in range(16):
        W.append([])
        W[i] = copy.deepcopy(Y[(i * 32):(i * 32 + 32)])

    for i in range(16, 80):
        W.append([])
        for j in range(32):
            W[i].append(W[i - 3][j] ^ W[i - 8][j] ^ W[i - 14][j] ^ W[i - 16][j])
        W[i] = int2list(copy.deepcopy(CLM(list2int(W[i], 32), 1)), 32)

    return W


def int2list(aInt, n):
    """
    将一个整型转为列表，存储其二进制比特位
    :param aInt: 整型数
    :param n: 二进制数的比特位数
    :return: 列表存储的二进制数
    """
    listValue = []
    for i in range(n):
        listValue.append((aInt >> (n - 1 - i)) & 0b1)
    return listValue


def list2int(aList, n):
    """
    将一个用列表存储的二进制数转为整型
    :param aList: 列表存储的二进制数
    :param n: 二进制数的比特位数
    :return: 整型的二进制数
    """
    intValue = 0
    for i in range(n):
        intValue = (intValue << 1) + aList[i]
    return intValue


def CLM(X, n):
    """
    对X进行循环移位
    :param X: 一个整数
    :param n: 循环移位位数
    :return: 循环移位后的整数
    """
    tmp = int2list(X, 32)
    X1 = tmp[n:32] + tmp[0:n]
    return list2int(X1, 32)


def f(t, b, c, d):
    """
    逻辑函数f
    :param t: 不同的步数对应不同的f
    :param b: 链接变量B
    :param c: 链接变量C
    :param d: 链接变量D
    :return: f函数结果
    """
    tmp_b = int2list(b, 32)
    tmp_c = int2list(c, 32)
    tmp_d = int2list(d, 32)
    res = []
    if t == 0:
        for i in range(32):
            res.append((tmp_b[i] & tmp_c[i]) | ((tmp_b[i] ^ 0b1) & tmp_d[i]))
    elif t == 1:
        for i in range(32):
            res.append((tmp_b[i] ^ tmp_c[i] ^ tmp_d[i]))
    elif t == 2:
        for i in range(32):
            res.append((tmp_b[i] & tmp_c[i]) | (tmp_b[i] & tmp_d[i]) | (tmp_c[i] & tmp_d[i]))
    elif t == 3:
        for i in range(32):
            res.append((tmp_b[i] ^ tmp_c[i] ^ tmp_d[i]))
    return list2int(res, 32)


def SHA1(S):
    """
    SHA-1安全Hash算法
    :param S: 输入的消息（字节串形式）
    :return: 160bit的Hash结果
    """
    global N, A, B, C, D, E
    N = 0
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476
    E = 0xc3d2e1f0
    K = [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6]

    M = copy.deepcopy(divide(S))

    for i in range(N + 1):  # 共N+1个消息分组
        a, b, c, d, e = A, B, C, D, E
        W = copy.deepcopy(extend(M[i]))
        for j in range(4):  # 对每个消息分组做4轮
            for k in range(20):  # 每轮20步
                a, b, c, d, e = (CLM(a, 5) + f(j, b, c, d) + e + list2int(W[j * 20 + k], 32) + K[j]) % 0x100000000, a, CLM(b, 30), c, d
        A, B, C, D, E = (a + A) % 0x100000000, (b + B) % 0x100000000, (c + C) % 0x100000000, (d + D) % 0x100000000, (e + E) % 0x100000000

    res = (A << 128) + (B << 96) + (C << 64) + (D << 32) + E
    # print(hex(res))
    return res


def testSHA1():
    """
    SHA-1算法测试函数
    :return:
    """
    fin = open("SHA1_testMsg.txt", "rb")
    S = fin.read()
    print("输入（字节串）：", S)

    res = SHA1(S)
    print("SHA-1的Hash结果：", hex(res))
    fin.close()


if __name__ == "__main__":
    print("--------SHA-1算法--------")
    testSHA1()
