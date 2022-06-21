# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 20:37
# @Author   : WZS
# @File     : AES_speedTest.py
# @Software : PyCharm
# @Function : AES测速


import AES
import time

key = 0x00000000000000000000000000000000

testTime = 10
totalTime = 0

for t in range(testTime):
    startTime = time.time()

    plainTextFile = open("testTxt_AES_500.txt", "r")
    data = plainTextFile.readlines()
    cipherText = []
    for i in range(len(data)):
        plainTextGroup = int(data[i][:-1], 16)
        cipherText.append(AES.encrypt(plainTextGroup, key))

    # # 将加密结果由比特串转为16进制字符文本
    # cipher = []
    # for i in range(len(data)):
    #     cipher.append(DES.printInHex(cipherText[i], 64))
    # print(cipher)

    endTime = time.time()
    totalTime += endTime - startTime
    print("AES完成第" + str(t) + "次对500个分组的加密！")
    print("耗时：" + str(endTime - startTime) + "s / 500个分组")
    plainTextFile.close()

print("平均用时：" + str(totalTime / 10) + "s / 500个分组")