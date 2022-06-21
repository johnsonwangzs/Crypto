import copy


flag = 0


def encode(txt, fout):
    global flag
    dic = {}
    curBytes = []
    index = 0  # 字典中总元素数
    # 建立字典，计算索引号的最大值（以确定编码时具体以多少比特位来表示索引号或段号）
    for aByte in txt:
        flag = 1
        curBytes.append(aByte)
        curTuple = tuple(curBytes)
        if curTuple not in dic:
            index += 1
            if len(curTuple) != 1:
                preTuple = curTuple[0:len(curTuple) - 1]
                dic[curTuple] = (index, dic[preTuple][0])  # 加入字典(索引号，段号）
            else:
                dic[curTuple] = (index, 0)
            curBytes = []

    if flag == 0:  # 空文件
        print("空文件！")
        return -1
    magicNumber(fout)  # 为编码后的输出文件添加Magic Number标记

    # 输出序号部分所占的二进制数的长度num
    num = 0
    while index > 0:
        num += 1
        index >>= 1
    fout.write(int(num).to_bytes(length=1, byteorder='little', signed=False))
    # 编码并输出
    curBytes = []
    dic1 = {}
    cnt = 0
    output = ''
    for aByte in txt:
        curBytes.append(aByte)
        curTuple = tuple(curBytes)
        if curTuple not in dic1:
            cnt += 1
            if len(curTuple) != 1:  # 如果非“新单个字符”
                preTuple = curTuple[0:len(curTuple) - 1]
                para = dic1[preTuple][0]  # 段号
                dic1[curTuple] = (cnt, para)  # 加入字典(索引号，段号）
                # 输出
                tmp = para
                js = 0
                # 段号部分
                while tmp > 0:  # 计算当前字符段号有效位的二进制长度
                    tmp >>= 1
                    js += 1
                for i in range(num - js):  # 不足num位的用0补齐
                    output += '0'
                for i in range(js):
                    output += str((para >> (js - 1 - i)) & 0b1)
                # 字符部分
                for i in range(8):  # 用一个字节来表示一个字符
                    output += str((aByte >> (7 - i)) & 0b1)
                # 输出
                while len(output) >= 8:  # 每8bit凑成一个byte输出
                    byteOut = 0
                    for i in range(8):
                        byteOut = (byteOut << 1) + ord(output[i]) - 48
                    fout.write(int(byteOut).to_bytes(length=1, byteorder='little', signed=False))
                    output = copy.deepcopy(output[8:])
            else:  # 如果是新的“单个字符”
                # 加入字典
                dic1[curTuple] = (cnt, 0)
                # 段号部分（全是0）
                for i in range(num):
                    output += '0'
                # 字符部分
                for i in range(8):
                    output += str((aByte >> (7 - i)) & 0b1)
                # 输出
                while len(output) >= 8:
                    byteOut = 0
                    for i in range(8):
                        byteOut = (byteOut << 1) + ord(output[i]) - 48
                    fout.write(int(byteOut).to_bytes(length=1, byteorder='little', signed=False))
                    output = copy.deepcopy(output[8:])
            curBytes = []
    if curBytes:  # 如果列表不为空，代表还需要特殊处理txt末尾的几个字符
        curTuple = tuple(curBytes)
        para = dic1[curTuple][0]  # 段号
        # 段号部分
        tmp = para
        js = 0
        while tmp > 0:  # 计算当前字符段号有效位的二进制长度
            tmp >>= 1
            js += 1
        for i in range(num - js):  # 不足num位的用0补齐
            output += '0'
        for i in range(js):
            output += str((para >> (js - 1 - i)) & 0b1)
        # 输出
        while len(output) >= 8:
            byteOut = 0
            for i in range(8):
                byteOut = (byteOut << 1) + ord(output[i]) - 48
            fout.write(int(byteOut).to_bytes(length=1, byteorder='little', signed=False))
            output = copy.deepcopy(output[8:])
    # 填充并输出剩余不满8位、尚未输出的比特
    # 在输出字节流的最后一个字节后额外增加一个字节，用来标记最后一个字节的位数
    if len(output) == 0:
        fout.write(int(8).to_bytes(length=1, byteorder='little', signed=False))
    else:
        byteOut = 0
        for i in range(len(output)):
            byteOut = (byteOut << 1) + ord(output[i]) - 48
        for i in range(8 - len(output)):
            byteOut = byteOut << 1
        fout.write(int(byteOut).to_bytes(length=1, byteorder='little', signed=False))
        fout.write(int(len(output)).to_bytes(length=1, byteorder='little', signed=False))


def magicNumber(fout):  # 为编码后的输出文件添加Magic Number标记
    fout.write(int(0).to_bytes(length=1, byteorder='little', signed=False))
    fout.write(int(4).to_bytes(length=1, byteorder='little', signed=False))
    fout.write(int(0).to_bytes(length=1, byteorder='little', signed=False))
    fout.write(int(9).to_bytes(length=1, byteorder='little', signed=False))


def goLZEnc():
    fin = open("testfile.txt", "rb")
    # fin = open("testfile1", "rb")
    # fin = open("testHexTxt.txt", "rb")
    # fin = open("pic.jpg", "rb")
    fout = open("encodedFile_LZ78", "wb")
    origTxt = fin.read()
    encode(origTxt, fout)
    if flag == 0:
        print("空文件！")
    fin.close()
    fout.close()


if __name__ == '__main__':
    goLZEnc()