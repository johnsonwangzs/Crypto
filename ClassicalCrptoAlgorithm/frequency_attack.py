"""
@author: WZS
功能：字母频率攻击（针对加法Caesar密码）
"""
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def encrypt(txt, k):
    m = list(txt)
    for i in range(len(txt)):
        if 'A' <= txt[i] <= 'Z':
            m[i] = chr(((ord(txt[i]) - 65) + k) % 26 + 97)  # 此处统一转为小写字母处理
        elif 'a' <= txt[i] <= 'z':
            m[i] = chr(((ord(txt[i]) - 97) + k) % 26 + 97)
    return ''.join(m)


def count(txt):
    # 统计字频
    clist = [0] * 26
    for ch in txt:
        if 'A' <= ch <= 'Z':
            clist[ord(ch) - 65] += 1
        elif 'a' <= ch <= 'z':
            clist[ord(ch) - 97] += 1
    return clist


def attack(txt):  # 对加密文本的字母频率攻击
    char_list = count(txt)
    # 查找密文中字母频率最高的字母
    max_freq = -1
    for i in range(26):
        if char_list[i] > max_freq:
            max_freq = char_list[i]
            flag = i
    k = ord('e') - 97 - i  # 密文中字母频率最高的，大概率对应于字母频率表中频率最高的'e'
    return k


def decrypt(txt, k):
    c = list(txt)
    for i in range(len(txt)):
        if 'a' <= txt[i] <= 'z':
            c[i] = chr(((ord(txt[i]) - 97) - k) % 26 + 97)
    return ''.join(c)


if __name__ == '__main__':
    print("--------加法Caesar密码字母频率攻击--------")
    # print("模式：1=加密原文 2=攻击密文。")
    # mode = eval(input("输入模式mode："))
    # if mode == 1:
    #     k = 5  # 加法密码移位数
    #     f_in = open("originalText.txt", "r", encoding='UTF-8')
    #     f_out = open("attack1_encryptedText.txt", "w", encoding='UTF-8')
    #     txt = f_in.read()
    #     encryptedTxt = encrypt(txt, k)
    #     f_out.write(encryptedTxt)
    #     f_in.close()
    #     f_out.close()
    # elif mode == 2:
    #     f_in = open("attack_encryptedText.txt", "r", encoding='UTF-8')
    #     f_out = open("attack_decryptedText.txt", "w", encoding='UTF-8')
    #     txt = f_in.read()
    #     k = attack(txt)
    #     decryptedTxt = decrypt(txt, k)
    #     f_out.write(decryptedTxt)
    #     f_in.close()
    #     f_out.close()

    graphviz = GraphvizOutput()
    graphviz.output_file = 'frequency_attack.png'
    with PyCallGraph(output=graphviz):
        k = 5  # 加法密码移位数
        f_in = open("originalText.txt", "r", encoding='UTF-8')
        f_out = open("attack_encryptedText.txt", "w", encoding='UTF-8')
        txt = f_in.read()
        encryptedTxt = encrypt(txt, k)
        f_out.write(encryptedTxt)
        f_in.close()
        f_out.close()
        f_in = open("attack_encryptedText.txt", "r", encoding='UTF-8')
        f_out = open("attack_decryptedText.txt", "w", encoding='UTF-8')
        txt = f_in.read()
        k = attack(txt)
        decryptedTxt = decrypt(txt, k)
        f_out.write(decryptedTxt)
        f_in.close()
        f_out.close()
