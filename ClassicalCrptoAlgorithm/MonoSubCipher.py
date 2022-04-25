# 单表代替密码
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def encrypt(m, f):
    m1 = list(m)
    for i in range(len(m)):
        m1[i] = f[ord(m[i]) - 97]
    return ''.join(m1)


def decrypt(c, f):
    c1 = list(c)
    for i in range(len(c)):
        p = f.find(c[i])  # p是密文字母在替换表中对应的下标
        c1[i] = chr(p + 97)
    return ''.join(c1)


if __name__ == '__main__':
    print("--------单表代替密码--------")
    # print("模式：1=加密（输入为明文m） 2=解密（输入为密文c）。")
    # mode = eval(input("输入模式mode："))
    # f = input("输入用于替换的单表f：")
    # if mode == 1:
    #     m = input("请输入要加密的明文m：")
    #     c = encrypt(m, f)
    #     print("加密后密文c为：", c)
    # elif mode == 2:
    #     c = input("请输入要解密的密文c：")
    #     m = decrypt(c, f)
    #     print("解密后明文m为：", m)

    graphviz = GraphvizOutput()
    graphviz.output_file = 'MonoSubCipher.png'
    with PyCallGraph(output=graphviz):
        print("\n加密doyouwannatodance\n-->{}".format(encrypt("doyouwannatodance", "qazwsxedcrfvtgbyhnujmiklop")))
        print("\n解密youcanreallydance\n-->{}".format(decrypt("youcanreallydance", "qazwsxedcrfvtgbyhnujmiklop")))