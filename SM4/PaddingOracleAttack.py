import oracle_SM4
import copy
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def divideCipher(txt):  # 拆分密文分组
    cnt, num, tmp = 0, 0, 0
    cipher = []
    for aByte in content:
        cnt += 1
        tmp = (tmp << 8) + aByte
        if cnt == 16:
            cipher.append(tmp)
            tmp = 0
            num += 1
            cnt = 0
    return num, cipher


mid = []  # 已经确认的部分


def paddingAttack(C, n, num):  # 尝试n位填充的攻击
    print("------------------------------------------")
    print("Now try {0} bytes' padding oracle attack of group {1}......".format(n, num))
    global mid
    pre = 0  # 已经确定的mid的部分字节 ^ 当前的padding填充
    # 计算已确定的部分
    for i in range(n - 1):
        tmp = mid[15 - i] ^ n
        pre += tmp << (8 * i)
    # 尝试请求解密
    for i in range(256):
        curTry = (i << ((n - 1) * 8)) + pre  # 尝试每种IV
        res = oracle_SM4.requestDecrypt(C, curTry)  # 请求解密服务器
        if res == "200":  # 合法
            mid[16 - n] = copy.deepcopy(i ^ n)  # 确定出mid的一字节
            print("# Find :", hex(curTry))
            break


def tryAttack(C, curIV, num):  # 对第num个密文分组C，在已知IV的情况下尝试攻击
    global mid
    for i in range(16):
        mid.append(0)
    for i in range(16):
        paddingAttack(C, i + 1, num)  # 尝试n位填充的攻击
    finalMid = 0
    for i in range(16):
        finalMid = (finalMid << 8) + mid[i]
    plainTxt = 0
    for i in range(128):
        plainTxt = (plainTxt << 1) + ((finalMid >> (127 - i)) & 0b1) ^ ((curIV >> (127 - i)) & 0b1)
    return plainTxt


if __name__ == '__main__':
    print("--------PaddingOracleAttack--------")
    # print("准备开始攻击，请输入要攻击的密文和所用初始IV：")
    # 从文件中提取密文
    fin = open("cipher-cbc", "rb")
    content = fin.read()
    num, cipherTxt = divideCipher(content)
    IV = 0x0123456789ABCDEFFEDCBA9876543210
    plaintext = []
    print("--------START TO ATTACK--------")
    curPlainTxt = 0
    for k in range(num):
        curPlainTxt = tryAttack(cipherTxt[k], IV, k + 1)
        print("get the No.{0} group's plaintext: {1}".format(k + 1, hex(curPlainTxt)))
        plaintext.append(curPlainTxt)
        IV = cipherTxt[k]
    print("\nAttack Succeeded!\nThe plaintext is:")
    for i in range(num - 1):
        for j in range(16):
            print("%02X" % ((plaintext[i] >> ((15 - j) * 8)) & 0xff), end=' ')
        print()
    paddingNum = plaintext[num - 1] & 0xff
    if paddingNum != 16:
        for i in range(16 - paddingNum):
            print("%02X" % ((plaintext[num - 1] >> ((15 - i) * 8)) & 0xff), end=' ')
    fin.close()