# 维吉尼亚密码
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def encrypt(m, key):
    p = 0  # 指示key中字符位置的指针
    m1 = list(m)
    for i in range(len(m)):
        if p == len(key):
            p = 0
        m1[i] = chr(((ord(m[i]) - 97)
                     + (ord(key[p]) - 97)) % 26 + 97)
        p += 1
    return ''.join(m1)


def decrypt(c, key):
    p = 0
    c1 = list(c)
    for i in range(len(c)):
        if p == len(key):
            p = 0
        c1[i] = chr(((ord(c[i]) - 97)
                     - (ord(key[p]) - 97)) % 26 + 97)
        p += 1
    return ''.join(c1)


if __name__ == '__main__':
    print("--------维吉尼亚密码--------")
    # print("模式：1=加密（输入为明文m） 2=解密（输入为密文c）。")
    # mode = eval(input("输入模式mode："))
    # key = input("输入密钥key：")
    # if mode == 1:
    #     m = input("请输入要加密的明文m：")
    #     c = encrypt(m, key)
    #     print("加密后密文c为：", c)
    # elif mode == 2:
    #     c = input("请输入要解密的密文c：")
    #     m = decrypt(c, key)
    #     print("解密后明文m为：", m)

    graphviz = GraphvizOutput()
    graphviz.output_file = 'Vigenere.png'
    with PyCallGraph(output=graphviz):
        print("\n加密zhonghuaminzuweidafuxing\n-->{}".format(encrypt("zhonghuaminzuweidafuxing", "interesting")))
        print("\n解密kqjyhynruwnadzmk\n-->{}".format(decrypt("kqjyhynruwnadzmk", "boring")))