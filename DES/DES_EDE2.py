# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 18:27
# @Author   : WZS
# @File     : DES_EDE2.py
# @Software : PyCharm
# @Function : 3DES算法


import DES

plainTxt = 0x1234567887654321
key1 = 0x0000000000000000
key2 = 0x1111111111111111

c1 = int(DES.printInHex(DES.encrypt(plainTxt, key1), 64), 16)
m = int(DES.printInHex(DES.decrypt(c1, key2), 64), 16)
c2 = DES.printInHex(DES.encrypt(m, key1), 64)

print("DES_EDE2加密完成！结果为：", c2)


cipherTxt = 0xed2491dc650edea3
key1 = 0x0000000000000000
key2 = 0x1111111111111111

m2 = int(DES.printInHex(DES.decrypt(cipherTxt, key1), 64), 16)
c = int(DES.printInHex(DES.encrypt(m2, key2), 64), 16)
m1 = DES.printInHex(DES.decrypt(c, key1), 64)

print("DES_EDE2解密完成！结果为：", m1)






