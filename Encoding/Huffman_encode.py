import copy


flag = 0  # 空文件处理标记


class Node:  # Huffman树节点类
    def __init__(self, info):
        self.aByte = info[0]  # 字符的字节值（从文本读入）
        self.freq = info[1]  # 对应字符频率（统计得到）
        self.lChild = None  # 左孩子
        self.rChild = None  # 右孩子
        self.code = ''


def getByteFreq(txt, fout):  # 按字节读入，统计频率，按出现次数排序
    global flag
    # 从原文中按字节取出，统计次数
    dic = {}
    for aByte in txt:
        flag = 1
        if aByte in dic:
            dic[aByte] += 1
        else:
            dic[aByte] = 1
    # 排除空文件干扰
    if flag == 0:
        return None
    magicNumber(fout)
    # 统计频率
    unsortedList = dic.items()
    sortedFreqQueue = sorted(unsortedList, key=lambda x: x[1], reverse=False)  # 按出现次数从小到大排序
    return sortedFreqQueue


def creatNodeQueue(bytelist):  # 根据节点类，构造树节点
    nodeQueue = []
    for each in bytelist:  # each为元组：(aByte，byteFreq)
        nodeQueue.append(Node(each))
    return nodeQueue


def creatHuffTree(bytelist):  # 构造Huffman树
    nodeQueue = creatNodeQueue(bytelist)  # 生成节点类的队列
    if len(nodeQueue) == 1:  # 此时整个文本只有一种字符，因此需要特殊考虑
        newNode = Node((bytelist[0][0], bytelist[0][1]))
        nodeQueue.append(newNode)
    while len(nodeQueue) != 1:
        # 从队列头部弹出频率最小的两个，合并后加入队列
        node_1 = nodeQueue.pop(0)
        node_2 = nodeQueue.pop(0)
        newNode = Node((None, node_1.freq + node_2.freq))
        newNode.lChild = node_1
        newNode.rChild = node_2
        if len(nodeQueue) == 0:
            nodeQueue.append(newNode)
        else:
            if newNode.freq > nodeQueue[len(nodeQueue) - 1].freq:
                nodeQueue.append(newNode)
            else:  # 需要保证加入新节点后，队列仍为从小到大的顺序
                for i in range(len(nodeQueue)):
                    if newNode.freq <= nodeQueue[i].freq:
                        nodeQueue = copy.deepcopy(nodeQueue[:i] + [newNode] + nodeQueue[i:])
                        break
    return nodeQueue.pop(0)


codeDic_c2B = {}  # 编码字典——键值对：(code:aByte)
codeDic_B2c = {}  # 编码字典——键值对：(aByte:code)


def encodeNode(curNode, curCode):  # 遍历所有节点，给节点编码
    global codeDic_c2B, codeDic_B2c
    if curNode:
        encodeNode(curNode.lChild, curCode + '0')
        curNode.code += curCode
        if curNode.lChild == None and curNode.rChild == None:  # 如果是叶子节点
            codeDic_c2B[curNode.code] = curNode.aByte
            codeDic_B2c[curNode.aByte] = curNode.code
        encodeNode(curNode.rChild, curCode + '1')


def encodeTxt(txt, fout):  # 编码、输出
    global codeDic_B2c, codeDic_B2c
    # 输出码表
    fout.write(int(len(codeDic_B2c) - 1).to_bytes(length=1, byteorder='little', signed=False))
    fout.write(ord('\n').to_bytes(length=1, byteorder='little', signed=False))
    fout.write(ord('\n').to_bytes(length=1, byteorder='little', signed=False))
    for key in codeDic_B2c:
        fout.write(int(key).to_bytes(length=1, byteorder='little', signed=False))
        fout.write(ord(' ').to_bytes(length=1, byteorder='little', signed=False))  # 规定码树输出阶段，以' '作为一行中字符与对应编码的分隔
        for i in codeDic_B2c[key]:
            fout.write(ord(i).to_bytes(length=1, byteorder='little', signed=False))
        fout.write(ord('\n').to_bytes(length=1, byteorder='little', signed=False))
        fout.write(ord('\n').to_bytes(length=1, byteorder='little', signed=False))  # 规定码树输出阶段，以连续两个'\n'表示结束了一个键值对的输出
    fout.write(ord('\n').to_bytes(length=1, byteorder='little', signed=False))
    fout.write(ord('\n').to_bytes(length=1, byteorder='little', signed=False))  # 全部码树输出完之后，再输出两个'\n'表示码树输出结束，之后输出的是编码后的原文
    # 编码原文
    encoded = ''
    for aByte in txt:
        encoded += codeDic_B2c[aByte]
    # 每8个0/1作为一个字节输出
    cnt = 0
    tmp = 0
    for ch in encoded:
        cnt += 1
        tmp = (tmp << 1) + ord(ch) - 48
        if cnt == 8:
            fout.write(int(tmp).to_bytes(length=1, byteorder='little', signed=False))
            cnt = 0
            tmp = 0
    # 处理最后可能存在的不足8bit的情况
    # 在输出字节流的最后一个字节后额外增加一个字节，用来标记最后一个字节的位数
    if cnt == 0:
        fout.write(int(8).to_bytes(length=1, byteorder='little', signed=False))
    else:
        for i in range(8 - cnt):
            tmp = tmp << 1
        fout.write(int(tmp).to_bytes(length=1, byteorder='little', signed=False))
        fout.write(int(cnt).to_bytes(length=1, byteorder='little', signed=False))


def magicNumber(fout):  # 为编码后的输出文件添加Magic Number标记
    fout.write(int(0).to_bytes(length=1, byteorder='little', signed=False))
    fout.write(int(4).to_bytes(length=1, byteorder='little', signed=False))
    fout.write(int(0).to_bytes(length=1, byteorder='little', signed=False))
    fout.write(int(9).to_bytes(length=1, byteorder='little', signed=False))


def goHufEnc():
    fin = open("testfile.txt", "rb")
    # fin = open("testfile1", "rb")
    # fin = open("testHexTxt.txt", "rb")
    fout = open("encodedFile_Huffman", "wb")
    origTxt = fin.read()
    sortedByte = getByteFreq(origTxt, fout)  # 按字节读入，统计频率，按出现次数排序
    if sortedByte is None:
        print("空文件!")
        return
    magicNumber(fout)  # 为编码后的输出文件添加Magic Number标记
    rootNode = creatHuffTree(sortedByte)  # 构造Huffman树
    encodeNode(rootNode, '')  # 给节点编码
    encodeTxt(origTxt, fout)  # 给原文编码，并将结果输出到文件
    fin.close()
    fout.close()


if __name__ == '__main__':
    goHufEnc()