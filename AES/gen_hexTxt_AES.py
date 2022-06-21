# -*- coding: utf-8 -*-
# @Time     : 2022/6/7 20:43
# @Author   : WZS
# @File     : gen_hexTxt_AES.py
# @Software : PyCharm
# @Function : 生成AES算法测试数据集文件

import random
import datetime
if __name__ == '__main__':
    fout = open("testTxt_AES_500.txt", "w")
    N = 500
    sTime = datetime.datetime.now()
    for i in range(N):
        x = []
        for i in range(32):
            a = random.randint(0, 15)
            if 10 <= a <= 15:
                x.append(chr(a + 97 - 10))
            else:
                x.append(chr(a + 48))
        fout.writelines('0x' + ''.join(x) + '\n')
    eTime = datetime.datetime.now()
    print(eTime - sTime)
    fout.close()