# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 19:56
# @Author   : WZS
# @File     : gen_hexTxt.py
# @Software : PyCharm
# @Function : 16进制大文件的生成，用于测试DES算法的速度

import random
import datetime
if __name__ == '__main__':
    fout = open("testTxt_DES_1000.txt", "w")
    N = 1000
    sTime = datetime.datetime.now()
    for i in range(N):
        x = []
        for i in range(16):
            a = random.randint(0, 15)
            if 10 <= a <= 15:
                x.append(chr(a + 97 - 10))
            else:
                x.append(chr(a + 48))
        fout.writelines('0x' + ''.join(x) + '\n')
    eTime = datetime.datetime.now()
    print(eTime - sTime)
    fout.close()
