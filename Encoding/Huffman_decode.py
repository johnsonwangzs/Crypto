class Node:  # Huffman树节点类
    def __init__(self, info):
        self.aByte = info[0]
        self.code = info[1]
        self.lChild = None
        self.rChild = None


rootNode = Node((None, None))
flag = 0  # 空文件标记


def addNode2Tree(curNode, newNode, code):
    if len(code) == 1:  # 加入叶子节点
        if code == '0':
            curNode.lChild = newNode
        elif code == '1':
            curNode.rChild = newNode
    else:
        if code[0] == '0':
            if not curNode.lChild:
                curNode.lChild = Node((None, None))
            addNode2Tree(curNode.lChild, newNode, code[1:])
        elif code[0] == '1':
            if not curNode.rChild:
                curNode.rChild = Node((None, None))
            addNode2Tree(curNode.rChild, newNode, code[1:])


def readFile(txt):
    global flag
    # 重构Huffman树
    cnt = 0  # 读取计数器
    flag_10 = 0  # 读取到换行符的标记
    flag_32 = 0  # 读取到空格符的标记
    curByte = 0
    curCode = 0
    magicNumList = [0, 4, 0, 9]
    origEncodedTxt = ''
    for aByte in txt:
        flag = 1
        if cnt < 4:
            if aByte != magicNumList[cnt]:  # magicNumber校验错误
                flag = 2
                return None
            cnt += 1
        else:
            if (flag_10 == 2 and flag_32 == 1) or (flag_10 == 2 and flag_32 == 2):  # 读字符对应编码
                if aByte != 32:
                    if aByte != 10:  # 如果此时读到的不是'\n'，说没编码还没读完
                        curCode += chr(aByte)  # 以字符串形式存储字符对应编码
                    else:  # 如果此时读到的是'\n'，说明编码已经读完，那么创建结点并加入树中
                        flag_10 = 0
                        flag_32 = 0
                        newNode = Node((curByte, curCode))
                        addNode2Tree(rootNode, newNode, curCode)
                else:  # ' '是当前行被编码的字符！
                    curByte = 32
                    curCode = ''
            if flag_10 == 3:  # 连续读到三个'\n'，代表'\n'是当前行被编码的字符！
                if flag_32 == 0:
                    curByte = 10
                    curCode = ''
                else:
                    if aByte != 10:
                        curCode += chr(aByte)
                    else:
                        flag_10 = 0
                        flag_32 = 0
                        newNode = Node((curByte, curCode))
                        addNode2Tree(rootNode, newNode, curCode)
            if aByte == 10 and flag_10 != 4:  # 读到'\n'
                flag_10 += 1
                continue
            if aByte == 32 and flag_10 != 4:  # 读到' '
                flag_32 += 1
                continue
            if flag_10 == 2 and flag_32 == 0:  # 读到一个新的字符，先记录下来
                curByte = aByte
                curCode = ''
                continue
            if flag_10 == 4:  # 码树读取结束标志
                tmp = ''
                for i in range(8):
                    tmp += str((aByte >> (7 - i)) & 0b1)
                origEncodedTxt += tmp
    if flag == 0:
        return None
    return origEncodedTxt


def findPath(curNode, ch):
    node = None
    if ch == '1':
        node = curNode.rChild
    elif ch == '0':
        node = curNode.lChild
    if node.lChild is None and node.rChild is None:  # 如果是叶子节点
        return node, 1
    else:
        return node, 0


def decode(txt, fout):
    global flag
    origEncodedTxt = readFile(txt)
    if flag == 0:  # 空文件
        print("空文件！")
        return -1
    elif flag == 2:  # Magic Number校验错误
        print("Magic Number校验错误！该文件可能不是由本程序编码得到！\n解码终止。")
        return -1
    else:
        # 特殊处理最后两个字节（用最后一个字节来确定倒数第二个字节的具体位数）
        num = 0
        for ch in origEncodedTxt[(len(origEncodedTxt) - 8):]:
            num = (num << 1) + ord(ch) - 48
        encodedTxt = origEncodedTxt[:(len(origEncodedTxt) - 16 + num)]
        i = 0
        curNode = rootNode
        while i < len(encodedTxt):
            curNode, isFind = findPath(curNode, encodedTxt[i])
            if isFind == 1:
                fout.write(int(curNode.aByte).to_bytes(length=1, byteorder='little', signed=False))
                curNode = rootNode
            i += 1


def goHufDec():
    fin = open("encodedFile_Huffman", "rb")
    fout = open("decodedFile_Huffman", "wb")
    origTxt = fin.read()
    decode(origTxt, fout)
    fin.close()
    fout.close()


if __name__ == '__main__':
    goHufDec()