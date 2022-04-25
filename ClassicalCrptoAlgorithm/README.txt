------文件名称及简介------

Affine.py：仿射密码
MonoSubCipher.py：单表代替密码
Vigenere.py：维吉尼亚密码
Vernam.py：弗纳姆密码
RailfenceCipher.py：栅栏密码
Hill.py：Hill密码
frequency_attack.py：字母频率攻击（针对加法Caesar密码）
Hill_attack.py：Hill密码已知明文攻击


------算法中包含或调用的函数名称及功能------

Affine.py:
    exEuclid():扩展欧几里得算法，用于求逆元
    encrypt():加密
    decrypt():解密
MonoSubCipher.py:
    encrypt():加密
    decrypt():解密
Vigenere.py:
    encrypt():加密
    decrypt():解密
Vernam.py:
    encrypt():加密
    decrypt():解密
RailfenceCipher.py:
    encrypt():加密
    decrypt():解密
Hill.py:
    encrypt(m, order, key_matrix):加密
    decrypt(c, order, key_matrix):解密
    AllRange(listx, start, end):产生全排列
    reverse_cnt(p, n):计算n个数的序列p的逆序数
    det(matrix, order):使用定义法计算order阶行列式matrix的值
    cal_M(matrix, order, x, y):计算order阶矩阵matrix中(x,y)位置元素的余子式
    multi_inverse(a, b):求a模b的乘法逆元
    inverse_matrix(matrix, order):求order阶矩阵matrix的逆矩阵
frequency_attack.py:
    encrypt(txt, k):用k作为加法密码中的密钥k对网上取得的英语文本进行加密处理，
                    得到一份测试密文（这个函数将原文中大小写的情况统一处理为小写）
    count(txt):统计文本中的字母频率
    attack(txt):对密文中的字母进行字频统计，返回可能的密钥k
    decrypt(txt, k):用可能的密钥k对密文进行解密
Hill_attack.py:
    check_isInv(m, order, choose_ch, choose_pos, used):全排列查找合适的（需可逆）明文矩阵
    attackHill(m, c, order):Hill密码已知明文攻击