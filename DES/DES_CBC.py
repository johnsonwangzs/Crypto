# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 19:57
# @Author   : WZS
# @File     : DES_CBC.py
# @Software : PyCharm
# @Function : DES_CBC模式


import DES

key = 0x0000000000000000
iv = 0x8765432187654321

plainTextFile = open("testTxt_DES_CBC.txt", "r")

data = plainTextFile.readlines()
cipherText = []

afterXor = 0
plainTextGroup = int(data[0][:-1], 16)
for i in range(64):
    afterXor = (afterXor << 1) + (((plainTextGroup >> (63 - i)) & 0b1) ^ ((iv >> (63 - i)) & 0b1))
cipherText.append(int(DES.printInHex(DES.encrypt(afterXor, key), 64), 16))

if len(data) > 1:
    for i in range(1, len(data)):
        plainTextGroup = int(data[i][:-1], 16)
        afterXor = 0
        for j in range(64):
            afterXor = (afterXor << 1) + (((plainTextGroup >> (63 - i)) & 0b1) ^ ((cipherText[i - 1] >> (63 - i)) & 0b1))
        cipherText.append(int(DES.printInHex(DES.encrypt(afterXor, key), 64), 16))

for i in range(len(cipherText)):
    print(hex(cipherText[i]))



