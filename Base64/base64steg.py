# -*- coding: utf-8 -*-
# @Time     : 2022/6/9 12:40
# @Author   : WZS
# @File     : b64steg_findHidden.py
# @Software : PyCharm
# @Function : base64解码；找出b64steg信息隐藏

import base64


b64_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
            'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
            'Z': 25, 'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36,
            'l': 37, 'm': 38, 'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48,
            'x': 49, 'y': 50, 'z': 51, '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60,
            '9': 61, '+': 62, '/': 63}
""" 
打印base64字符映射关系字典
print("{", end='')
for i in range(26):
    print("'" + str(chr(65 + i)) + "':" + str(i) + ",", end='')
for i in range(26):
    print("'" + str(chr(97 + i)) + "':" + str(i + 26) + ",", end='')
for i in range(10):
    print("'" + str(chr(48 + i)) + "':" + str(i + 52) + ",", end='')
print("'+':62, '/':63", end='')
print("}")
"""


def dec2bin(num, n):
    """
    十进制转二进制
    :param num: 十进制数
    :param n: 比特位数
    :return: 二进制列表
    """
    res = []
    for i in range(n):
        res.append((num >> (n - i - 1)) & 0b1)
    return res


def findHidden(data_b64):
    """
    提取隐藏信息
    :param data_b64: 原base64字串
    :return:
    """
    bitList = []
    for i in range(len(data_b64)):
        if data_b64[i].endswith('\n'):
            data_b64[i] = data_b64[i][:-1]
        for j in range(0, len(data_b64[i]), 4):  # 每4个b64编码字符作为一个切片处理
            b64Slice = data_b64[i][j:j + 4]
            asciiSlice = base64.b64decode(b64Slice)  # 正常解码
            f2.write(asciiSlice)
            if b64Slice.find("=") != -1:  # 含有等号的，做了填充，可能存在信息隐藏
                b64Slice_re = base64.b64encode(asciiSlice).decode()  # 将b64解码后的重新b64编码
                print(b64Slice)
                if b64Slice.find("==") != -1:  # 含有==填充的
                    pos = 1  # 可能导致信息隐藏的字符下标
                    n = 4  # 可能含信息隐藏的比特位数
                else:  # 含=填充的
                    pos = 2
                    n = 2
                ch_ord = b64_dict[b64Slice[pos]]
                ch_ord_re = b64_dict[b64Slice_re[pos]]
                diff_bit = dec2bin(ch_ord ^ ch_ord_re, n)
                bitList.extend(diff_bit)
                print(b64Slice_re)
                print(diff_bit)
                print()
    print(bitList, end='\n\n')
    ansBit = ''
    for i in range(len(bitList)):
        ansBit += str(bitList[i])
    return ''.join([chr(int(ansBit[i:i + 8], 2)) for i in range(0, len(ansBit), 8)])  # 8bit一组转为字符


if __name__ == "__main__":
    f1 = open("b64steg.txt", "r")
    f2 = open("b64steg_dec.txt", "wb")

    data_b64 = f1.readlines()
    print("flag{" + findHidden(data_b64) + "}")

    f1.close()
    f2.close()
