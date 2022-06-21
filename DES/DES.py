# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 18:27
# @Author   : WZS
# @File     : DES.py
# @Software : PyCharm
# @Function : 原始DES算法

import copy


IP_list = \
    [58, 50, 42, 34, 26, 18, 10, 2,
     60, 52, 44, 36, 28, 20, 12, 4,
     62, 54, 46, 38, 30, 22, 14, 6,
     64, 56, 48, 40, 32, 24, 16, 8,
     57, 49, 41, 33, 25, 17, 9, 1,
     59, 51, 43, 35, 27, 19, 11, 3,
     61, 53, 45, 37, 29, 21, 13, 5,
     63, 55, 47, 39, 31, 23, 15, 7]

IIP_list = \
    [40, 8, 48, 16, 56, 24, 64, 32,
     39, 7, 47, 15, 55, 23, 63, 31,
     38, 6, 46, 14, 54, 22, 62, 30,
     37, 5, 45, 13, 53, 21, 61, 29,
     36, 4, 44, 12, 52, 20, 60, 28,
     35, 3, 43, 11, 51, 19, 59, 27,
     34, 2, 42, 10, 50, 18, 58, 26,
     33, 1, 41, 9, 49, 17, 57, 25]

ls_list = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

pc1_list = \
    [57, 49, 41, 33, 25, 17, 9,
     1, 58, 50, 42, 34, 26, 18,
     10, 2, 59, 51, 43, 35, 27,
     19, 11, 3, 60, 52, 44, 36,
     63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
     14, 6, 61, 53, 45, 37, 29,
     21, 13, 5, 28, 20, 12, 4]

pc2_list = \
    [14, 17, 11, 24, 1, 5, 3, 28,
     15, 6, 21, 10, 23, 19, 12, 4,
     26, 8, 16, 7, 27, 20, 13, 2,
     41, 52, 31, 37, 47, 55, 30, 40,
     51, 45, 33, 48, 44, 49, 39, 56,
     34, 53, 46, 42, 50, 36, 29, 32]

e_List = \
    (32, 1, 2, 3, 4, 5, 4, 5,  # E盒
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1)

s_list = \
    [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

     [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

     [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

     [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

     [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

     [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

     [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

     [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

p_list = \
    [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

key_list = []


def IP(x):
    """
    IP置换
    :param x:
    :return:
    """
    y = []
    for i in range(64):
        y.append(x[IP_list[i] - 1])
    return y


def genKey(key):
    """
    DES密钥生成算法
    :param key: 64b密钥
    :return: 16个轮密钥
    """
    # 从左到右取出key的二进制位
    key_bin = []
    for i in range(64):
        key_bin.append((key >> (64 - i - 1)) & 1)
    # PC1置换
    key_afterPC1 = []
    for i in range(56):
        key_afterPC1.append(key_bin[pc1_list[i] - 1])
    # 分为c_0和d_0两部分
    c_0, d_0 = [], []
    for i in range(28):
        c_0.append(key_afterPC1[i])
        d_0.append(key_afterPC1[28 + i])
    # 进行16轮轮密钥生成
    c_pre, d_pre = c_0, d_0
    for i in range(16):
        # 循环左移
        ls = ls_list[i]
        if ls == 1:
            tmp_c, tmp_d = c_pre[0], d_pre[0]
            for j in range(27):
                c_pre[j], d_pre[j] = c_pre[j + 1], d_pre[j + 1]
            c_pre[27], d_pre[27] = tmp_c, tmp_d
        elif ls == 2: 
            tmp_c1, tmp_c2 = c_pre[0], c_pre[1]
            tmp_d1, tmp_d2 = d_pre[0], d_pre[1]
            for j in range(26):
                c_pre[j], d_pre[j] = c_pre[j + 2], d_pre[j + 2]
            c_pre[26], c_pre[27] = tmp_c1, tmp_c2
            d_pre[26], d_pre[27] = tmp_d1, tmp_d2
        # PC2置换
        tmp = c_pre + d_pre
        key_afterPC2 = []
        for j in range(48):
            key_afterPC2.append(tmp[pc2_list[j] - 1])
        key_list.append(key_afterPC2)


def extend(x):
    """
    E盒扩展
    :param x: 32b输入
    :return: 48b输出
    """
    y = []
    for i in range(48):
        y.append(x[e_List[i] - 1])
    return y


def xorRoundKey(x, r):
    """
    轮密钥加
    :param x: 48b输入
    :param r: 轮数
    :return: 48b输出
    """
    y = []
    for i in range(48):
        y.append(x[i] ^ key_list[r][i])
    return y


def sbox(x):
    """
    S盒
    :param x: 48b S盒输入
    :return: 32b输出
    """
    y = []
    for i in range(8):
        tmp = []
        for j in range(6):  # 取出第i组，每组6位，共8组
            tmp.append(x[i * 6 + j])
        row = tmp[0] * 2 + tmp[5]
        column = tmp[1] * 8 + tmp[2] * 4 + tmp[3] * 2 + tmp[4]
        s = s_list[i][row][column]
        for j in range(4):
            y.append((s >> (3 - j)) & 1)
    return y


def pbox(x):
    """
    P盒
    :param x: 32b S盒输出
    :return: 32b输出
    """
    y = []
    for i in range(32):
        y.append(x[p_list[i] - 1])
    return y


def F_en(afterIP):
    """
    加密轮函数
    :param afterIP: IP置换后结果
    :return: 16轮之后结果
    """
    # 初始值换后划分为l0和r0两部分
    l_0, r_0 = [], []
    for i in range(32):
        l_0.append(afterIP[i])
        r_0.append(afterIP[32 + i])
    # 进行16轮迭代
    r, l = r_0, l_0
    for i in range(16):
        l_nxt = copy.deepcopy(r)  # 深拷贝，易出bug！
        afterExtend = extend(r)
        afterXorKey = xorRoundKey(afterExtend, i)
        afterSbox = sbox(afterXorKey)
        afterPbox = pbox(afterSbox)
        for j in range(32):
            r[j] = afterPbox[j] ^ l[j]
        l = l_nxt
    return r + l  # 此处多左右交换一次


def F_de(afterIP):
    """
    解密轮函数
    :param afterIP: IP（逆）置换后结果
    :return: 16轮之后结果
    """
    # 初始值换后划分为l0和r0两部分
    l_0, r_0 = [], []
    for i in range(32):
        l_0.append(afterIP[i])
        r_0.append(afterIP[32 + i])
    # 进行16轮迭代
    r, l = r_0, l_0
    for i in range(15, -1, -1):  # 解密与加密唯一的区别是密钥倒着使用
        l_nxt = copy.deepcopy(r)  # 深拷贝，易出bug！
        afterExtend = extend(r)
        afterXorKey = xorRoundKey(afterExtend, i)
        afterSbox = sbox(afterXorKey)
        afterPbox = pbox(afterSbox)
        for j in range(32):
            r[j] = afterPbox[j] ^ l[j]
        l = l_nxt
    return r + l  # 此处多左右交换一次


def IIP(x):
    """
    IP逆置换
    :param x:
    :return:
    """
    y = []
    for i in range(64):
        y.append(x[IIP_list[i] - 1])
    return y


def encrypt(plainTxt, key):
    """
    DES加密
    :param plainTxt: 64b明文
    :param key: 64b密钥
    :return: 64b密文
    """
    global key_list
    key_list = []
    tmp = []
    for i in range(64):
        tmp.append((plainTxt >> (64 - i - 1)) & 1)  # 从左到右取出m的二进制位
    # IP置换
    afterIP = IP(tmp)
    # 轮函数
    genKey(key)  # 产生16组轮密钥
    afterF = F_en(afterIP)
    # IP逆置换
    cipherTxt = IIP(afterF)
    return cipherTxt


def decrypt(cipherTxt, key):
    """
    DES解密
    :param cipherTxt: 64b密文
    :param key: 64b密钥
    :return: 64b明文
    """
    global key_list
    key_list = []
    tmp = []
    for i in range(64):
        tmp.append((cipherTxt >> (64 - i - 1)) & 1)  # 从左到右取出m的二进制位
    # IP置换
    afterIP = IP(tmp)
    # 轮函数
    genKey(key)  # 产生16组轮密钥
    afterF = F_de(afterIP)
    # IP逆置换
    plainTxt = IIP(afterF)
    return plainTxt


def printInHex(x, n):
    """
    16进制输出
    :param x: 比特串
    :param n: x位数
    :return: 16进制形式
    """
    s = 0
    for i in range(n):
        s = (s << 1) + x[i]
    return hex(s)


if __name__ == '__main__':
    print("--------DES--------")
    # mode = eval(input("请输入模式（0=加密，1=解密）："))
    # key = eval(input("请输入密钥（16进制）："))
    # if mode == 0:
    #     plainTxt = eval(input("请输入明文（16进制）："))
    #     c = encrypt(plainTxt, key)
    #     printInHex(c, 64)
    # elif mode == 1:
    #     cipherTxt = eval(input("请输入密文（16进制）："))
    #     m = decrypt(cipherTxt, key)
    #     printInHex(m, 64)

    plainTxt = 0xffffffffffffffff
    key = 0x0000000000000000
    c = encrypt(plainTxt, key)
    print("加密完成！密文是：")
    print(printInHex(c, 64))

    cipherTxt = 0x355550b2150e2451
    key = 0x0000000000000000
    m = decrypt(cipherTxt, key)
    print("解密完成！明文是：")
    print(printInHex(m, 64))















