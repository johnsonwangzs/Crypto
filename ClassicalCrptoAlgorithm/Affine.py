# 仿射密码
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, xtmp, ytmp = extended_gcd(b, a % b)
        x = ytmp
        y = xtmp - int(a // b) * ytmp
        return gcd, x, y


def encrypt(m, k, b):
    m1 = list(m)
    for i in range(len(m)):  # 此处默认m中字母均为小写
        m1[i] = chr(((ord(m[i]) - 97) * k + b) % 26 + 97)
    return ''.join(m1)  # 列表转字符串


def decrypt(c, k, b):
    temp1, k1, temp2 = extended_gcd(k, 26)
    c1 = list(c)
    for i in range(len(c)):
        c1[i] = chr(((ord(c[i]) - 97 - b) * k1) % 26 + 97)
    return ''.join(c1)


if __name__ == '__main__':
    print("--------仿射密码--------")
    # print("模式：1=加密（输入为明文m） 2=解密（输入为密文c）。")
    # mode = eval(input("输入模式mode："))
    # k = eval(input("输入常数k："))
    # b = eval(input("输入常数b："))
    # legal_k = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    # if k in legal_k:
    #     if mode == 1:
    #         m = input("请输入要加密的明文m：")
    #         c = encrypt(m, k, b)
    #         print("加密后密文c为：", c)
    #     elif mode == 2:
    #         c = input("请输入要解密的密文c：")
    #         m = decrypt(c, k, b)
    #         print("解密后明文m为：", m)
    # else:
    #     print("k不合法！")

    graphviz = GraphvizOutput()
    graphviz.output_file = 'Affine.png'
    with PyCallGraph(output=graphviz):
        print("\n加密cryptography\n-->{}".format(encrypt("cryptography", 7, 10)))
        print("\n加密seeyoutomorrow\n-->{}".format(encrypt("seeyoutomorrow", 9, 13)))
        print("\n解密thisisciphertext\n-->{}".format(decrypt("thisisciphertext", 15, 20)))
        print("\n加密abcdef\n-->{}".format(encrypt("abcdef", 2, 1)))
