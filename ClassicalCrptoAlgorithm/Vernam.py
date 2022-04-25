# 弗纳姆密码
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def encrypt(m, key):
    c = []
    for i in range(len(m)):
        c.append(chr(ord(m[i]) ^ ord(key[i])))
    return ''.join(c)


def decrypt(c, key):
    m = []
    for i in range(len(c)):
        if c[i] == '\n':
            m.append(chr(ord('\r') ^ ord(key[i])))
        else:
            m.append(chr(ord(c[i]) ^ ord(key[i])))
    return ''.join(m)


if __name__ == '__main__':
    print("--------弗纳姆密码--------")
    print("输出见文件")
    # print("模式：1=加密（输入为明文m） 2=解密（输入为密文c）。")
    # mode = eval(input("输入模式mode："))
    # key = eval(input("输入密钥key："))
    # if mode == 1:
    #     m = input("请输入要加密的明文m：")
    #     c = encrypt(m, key)
    #     print("加密后密文c为：", c)
    # elif mode == 2:
    #     c = input("请输入要解密的密文c：")
    #     m = decrypt(c, key)
    #     print("解密后明文m为：", m)
    graphviz = GraphvizOutput()
    graphviz.output_file = 'Vernam.png'
    with PyCallGraph(output=graphviz):
        f_in1 = open("Vernam_input1.txt", "r", encoding='UTF-8')
        f_out1 = open("Vernam_output1.txt", "w", encoding='UTF-8')
        m = f_in1.read()
        f_out1.write(encrypt(m, "Todayis20200308"))
        f_in1.close()
        f_out1.close()

        f_in2 = open("Vernam_input2.txt", "r", encoding='UTF-8')
        f_out2 = open("Vernam_output2.txt", "w", encoding='UTF-8')
        c = f_in2.read()
        f_out2.write(decrypt(c, "12345abcde"))
        f_in2.close()
        f_out2.close()



