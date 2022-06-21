# -*- coding: utf-8 -*-
# @Time     : 2022/6/9 12:22
# @Author   : WZS
# @File     : b64steg_solution.py
# @Software : PyCharm
# @Function : 自动化解b64steg脚本

import base64

f1 = open("b64steg.txt", "r")
f2 = open("b64steg_dec.txt", "wb")
base64.decode(f1, f2)
f1.close()
f2.close()