# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 19:56
# @Author   : WZS
# @File     : DES_EDE2_speedTest.py
# @Software : PyCharm
# @Function : DES_EDE2算法加密速度测试

import DES
import time

key1 = 0x0000000000000000
key2 = 0x1111111111111111

testTime = 10
totalTime = 0

for t in range(testTime):
    startTime = time.time()

    plainTextFile = open("testTxt_DES_1000.txt", "r")
    data = plainTextFile.readlines()
    cipherText = []
    for i in range(len(data)):
        plainTextGroup = int(data[i][:-1], 16)
        c1 = int(DES.printInHex(DES.encrypt(plainTextGroup, key1), 64), 16)
        m = int(DES.printInHex(DES.decrypt(c1, key2), 64), 16)
        c2 = DES.encrypt(m, key1)
        cipherText.append(c2)

    # # 将加密结果由比特串转为16进制字符文本
    # cipher = []
    # for i in range(len(data)):
    #     cipher.append(DES.printInHex(cipherText[i], 64))
    # print(cipher)

    endTime = time.time()
    totalTime += endTime - startTime
    print("DES_EDE2完成第" + str(t) + "次对1000个分组的加密！")
    print("耗时：" + str(endTime - startTime) + "s / 1000个分组")
    plainTextFile.close()

print("平均用时：" + str(totalTime / 10) + "s / 1000个分组")