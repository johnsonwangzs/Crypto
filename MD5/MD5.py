# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 20:43
# @Author   : WZS
# @File     : MD5.py
# @Software : PyCharm
# @Function : MD5算法


mdValue = ""
message = ""

A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476
init_A = 0x67452301
init_B = 0xEFCDAB89
init_C = 0x98BADCFE
init_D = 0x10325476

# 64次子循环 设置常数表T
T = [0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE, 0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
     0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE, 0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
     0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA, 0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
     0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED, 0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
     0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C, 0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
     0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05, 0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
     0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039, 0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
     0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1, 0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391]

# 4轮 循环左移位数
s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
     5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
     4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
     6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

# 4轮 消息原文编号
m = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
     1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
     5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2,
     0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]


def F(X, Y, Z):
    return (X & Y) | ((~X) & Z)


def G(X, Y, Z):
    return (X & Z) | (Y & (~Z))


def H(X, Y, Z):
    return X ^ Y ^ Z


def I(X, Y, Z):
    return Y ^ (X | (~Z))


# 附加填充位
def fill_text():
    global mdValue
    for i in range(len(message)):
        c = int2bin(ord(message[i]), 8)
        mdValue += c

    if (len(mdValue) % 512 != 448):
        if ((len(mdValue) + 1) % 512 != 448):
            mdValue += '1'
        while (len(mdValue) % 512 != 448):
            mdValue += '0'

    length = len(message) * 8
    if (length <= 255):
        length = int2bin(length, 8)
    else:
        length = int2bin(length, 16)
        temp = length[8:12] + length[12:16] + length[0:4] + length[4:8]
        length = temp

    mdValue += length
    while (len(mdValue) % 512 != 0):
        mdValue += '0'


# 循环移位
def circuit_shift(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


# 换位
def change_pos():
    global A, B, C, D
    a = A
    b = B
    c = C
    d = D
    A = d
    B = a
    C = b
    D = c


def FF(mj, s, ti):
    global A, B, C, D
    mj = int(mj, 2)
    temp = F(B, C, D) + A + mj + ti
    temp = circuit_shift(temp, s)
    A = (B + temp) % pow(2, 32)
    change_pos()


def GG(mj, s, ti):
    global A, B, C, D
    mj = int(mj, 2)
    temp = G(B, C, D) + A + mj + ti
    temp = circuit_shift(temp, s)
    A = (B + temp) % pow(2, 32)
    change_pos()


def HH(mj, s, ti):
    global A, B, C, D
    mj = int(mj, 2)
    temp = H(B, C, D) + A + mj + ti
    temp = circuit_shift(temp, s)
    A = (B + temp) % pow(2, 32)
    change_pos()


def II(mj, s, ti):
    global A, B, C, D
    mj = int(mj, 2)
    temp = I(B, C, D) + A + mj + ti
    temp = circuit_shift(temp, s)
    A = (B + temp) % pow(2, 32)
    change_pos()


# 类型转换
def int2bin(n, count=24):
    return "".join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])


# MD5流程控制
def process():
    global A, B, C, D
    M = []
    for i in range(0, 512, 32):
        num = ""
        # 获取每一段的标准十六进制形式
        for j in range(0, len(mdValue[i:i + 32]), 4):
            temp = mdValue[i:i + 32][j:j + 4]
            temp = hex(int(temp, 2))
            num += temp[2]
        # 对十六进制进行小端排序
        num_tmp = ""
        for j in range(8, 0, -2):
            temp = num[j - 2:j]
            num_tmp += temp

        num = ""
        for i in range(len(num_tmp)):
            num += int2bin(int(num_tmp[i], 16), 4)
        M.append(num)

    FF(M[m[0]], s[0], T[0])
    FF(M[m[1]], s[1], T[1])
    FF(M[m[2]], s[2], T[2])
    FF(M[m[3]], s[3], T[3])
    FF(M[m[4]], s[4], T[4])
    FF(M[m[5]], s[5], T[5])
    FF(M[m[6]], s[6], T[6])
    FF(M[m[7]], s[7], T[7])
    FF(M[m[8]], s[8], T[8])
    FF(M[m[9]], s[9], T[9])
    FF(M[m[10]], s[10], T[10])
    FF(M[m[11]], s[11], T[11])
    FF(M[m[12]], s[12], T[12])
    FF(M[m[13]], s[13], T[13])
    FF(M[m[14]], s[14], T[14])
    FF(M[m[15]], s[15], T[15])

    GG(M[m[16]], s[16], T[16])
    GG(M[m[17]], s[17], T[17])
    GG(M[m[18]], s[18], T[18])
    GG(M[m[19]], s[19], T[19])
    GG(M[m[20]], s[20], T[20])
    GG(M[m[21]], s[21], T[21])
    GG(M[m[22]], s[22], T[22])
    GG(M[m[23]], s[23], T[23])
    GG(M[m[24]], s[24], T[24])
    GG(M[m[25]], s[25], T[25])
    GG(M[m[26]], s[26], T[26])
    GG(M[m[27]], s[27], T[27])
    GG(M[m[28]], s[28], T[28])
    GG(M[m[29]], s[29], T[29])
    GG(M[m[30]], s[30], T[30])
    GG(M[m[31]], s[31], T[31])

    HH(M[m[32]], s[32], T[32])
    HH(M[m[33]], s[33], T[33])
    HH(M[m[34]], s[34], T[34])
    HH(M[m[35]], s[35], T[35])
    HH(M[m[36]], s[36], T[36])
    HH(M[m[37]], s[37], T[37])
    HH(M[m[38]], s[38], T[38])
    HH(M[m[39]], s[39], T[39])
    HH(M[m[40]], s[40], T[40])
    HH(M[m[41]], s[41], T[41])
    HH(M[m[42]], s[42], T[42])
    HH(M[m[43]], s[43], T[43])
    HH(M[m[44]], s[44], T[44])
    HH(M[m[45]], s[45], T[45])
    HH(M[m[46]], s[46], T[46])
    HH(M[m[47]], s[47], T[47])

    II(M[m[48]], s[48], T[48])
    II(M[m[49]], s[49], T[49])
    II(M[m[50]], s[50], T[50])
    II(M[m[51]], s[51], T[51])
    II(M[m[52]], s[52], T[52])
    II(M[m[53]], s[53], T[53])
    II(M[m[54]], s[54], T[54])
    II(M[m[55]], s[55], T[55])
    II(M[m[56]], s[56], T[56])
    II(M[m[57]], s[57], T[57])
    II(M[m[58]], s[58], T[58])
    II(M[m[59]], s[59], T[59])
    II(M[m[60]], s[60], T[60])
    II(M[m[61]], s[61], T[61])
    II(M[m[62]], s[62], T[62])
    II(M[m[63]], s[63], T[63])

    A = (A + init_A) % pow(2, 32)
    B = (B + init_B) % pow(2, 32)
    C = (C + init_C) % pow(2, 32)
    D = (D + init_D) % pow(2, 32)

    answer = ""
    for each in [A, B, C, D]:
        each = hex(each)[2:]
        for i in range(8, 0, -2):
            answer += str(each[i - 2:i])

    return answer


if __name__ == "__main__":
    # message = input("输入原文：")
    f = open("testTxt_MD5_1000.txt", "r")
    message = f.read()
    fill_text()
    result = process()
    print("MD5:", format(result))
    f.close()
