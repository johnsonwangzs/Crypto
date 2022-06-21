import copy


flag1 = -1  # 空文件标记


def readFile(txt):
    global flag1
    flag = -1  # 读取计数器
    num = 0
    origEncodedTxt = ''
    magicNumList = [0, 4, 0, 9]
    for aByte in txt:
        if flag < 3:
            flag1 = 0
            if aByte != magicNumList[flag + 1]:  # Magic Number校验失败
                flag1 = 2
                return None, None
            flag += 1
        elif flag == 3:  # 编码后文件(除去Magic Num之后）的第一个字节用来存储段号部分的二进制长度
            num = aByte
            flag = 4
        else:
            for i in range(8):
                origEncodedTxt += str((aByte >> (7 - i)) & 0b1)
    if flag1 == -1:
        return None, None  # 空文件
    return num, origEncodedTxt


def decode(txt, fout):
    # 从文件中获取比特流
    num, origEncodedTxt = readFile(txt)
    if flag1 == -1:
        print("空文件！")
        return -1
    elif flag1 == 2:
        print("Magic Number校验错误！该文件可能不是由本程序编码得到！\n解码终止。")
        return -1
    # 特殊处理最后两个字节（用最后一个字节来确定倒数第二个字节的具体位数）
    cnt = 0
    for ch in origEncodedTxt[(len(origEncodedTxt) - 8):]:
        cnt = (cnt << 1) + ord(ch) - 48
    encodedTxt = origEncodedTxt[:(len(origEncodedTxt) - 16 + cnt)]
    # 解码
    cnt = 0  # 当前轮读了多少bit
    flag = 0  # flag为0代表正在读取num(bit)的段号 flag为1代表正在读取8(bit)的字符编码
    cur = 0  # 当前轮读得数值
    tmp = 0  # 临时存放每轮读完的段号
    index = -1  # 索引号
    indexList = []  # 索引表
    for ch in encodedTxt:
        cnt += 1
        cur = (cur << 1) + ord(ch) - 48
        if flag == 0 and cnt == num:  # 读到了一个完整的段
            if cur == 0:  # 代表是新的单字
                tmp = 0
            else:
                tmp = cur
            flag, cnt, cur = 1, 0, 0
        if flag == 1 and cnt == 8:  # 读到了一个完整的字符
            index += 1
            if tmp == 0:  # 代表是新的单字
                curList = copy.deepcopy([cur, ])
                indexList.append(curList)
                fout.write(int(cur).to_bytes(length=1, byteorder='little', signed=False))
            else:
                curList = copy.deepcopy(indexList[tmp - 1])
                curList.append(cur)
                indexList.append(curList)
                for i in curList:
                    fout.write(int(i).to_bytes(length=1, byteorder='little', signed=False))
            flag, cnt, cur, tmp = 0, 0, 0, 0
    if flag == 1 and tmp != 0:
        curList = copy.deepcopy(indexList[tmp - 1])
        for i in curList:
            fout.write(int(i).to_bytes(length=1, byteorder='little', signed=False))


def goLZDec():
    fin = open("encodedFile_LZ78", "rb")
    fout = open("decodedFile_LZ78", "wb")
    origTxt = fin.read()
    decode(origTxt, fout)
    fin.close()
    fout.close()


if __name__ == '__main__':
    goLZDec()
