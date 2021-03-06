"""
ZUC_128算法
"""


import copy

D = \
    [0b100010011010111, 0b010011010111100, 0b110001001101011, 0b001001101011110,
     0b101011110001001, 0b011010111100010, 0b111000100110101, 0b000100110101111,
     0b100110101111000, 0b010111100010011, 0b110101111000100, 0b001101011110001,
     0b101111000100110, 0b011110001001101, 0b111100010011010, 0b100011110101100]

S0 = \
    [[0x3E, 0x72, 0x5B, 0x47, 0xCA, 0xE0, 0x00, 0x33, 0x04, 0xD1, 0x54, 0x98, 0x09, 0xB9, 0x6D, 0xCB],
     [0x7B, 0x1B, 0xF9, 0x32, 0xAF, 0x9D, 0x6A, 0xA5, 0xB8, 0x2D, 0xFC, 0x1D, 0x08, 0x53, 0x03, 0x90],
     [0x4D, 0x4E, 0x84, 0x99, 0xE4, 0xCE, 0xD9, 0x91, 0xDD, 0xB6, 0x85, 0x48, 0x8B, 0x29, 0x6E, 0xAC],
     [0xCD, 0xC1, 0xF8, 0x1E, 0x73, 0x43, 0x69, 0xC6, 0xB5, 0xBD, 0xFD, 0x39, 0x63, 0x20, 0xD4, 0x38],
     [0x76, 0x7D, 0xB2, 0xA7, 0xCF, 0xED, 0x57, 0xC5, 0xF3, 0x2C, 0xBB, 0x14, 0x21, 0x06, 0x55, 0x9B],
     [0xE3, 0xEF, 0x5E, 0x31, 0x4F, 0x7F, 0x5A, 0xA4, 0x0D, 0x82, 0x51, 0x49, 0x5F, 0xBA, 0x58, 0x1C],
     [0x4A, 0x16, 0xD5, 0x17, 0xA8, 0x92, 0x24, 0x1F, 0x8C, 0xFF, 0xD8, 0xAE, 0x2E, 0x01, 0xD3, 0xAD],
     [0x3B, 0x4B, 0xDA, 0x46, 0xEB, 0xC9, 0xDE, 0x9A, 0x8F, 0x87, 0xD7, 0x3A, 0x80, 0x6F, 0x2F, 0xC8],
     [0xB1, 0xB4, 0x37, 0xF7, 0x0A, 0x22, 0x13, 0x28, 0x7C, 0xCC, 0x3C, 0x89, 0xC7, 0xC3, 0x96, 0x56],
     [0x07, 0xBF, 0x7E, 0xF0, 0x0B, 0x2B, 0x97, 0x52, 0x35, 0x41, 0x79, 0x61, 0xA6, 0x4C, 0x10, 0xFE],
     [0xBC, 0x26, 0x95, 0x88, 0x8A, 0xB0, 0xA3, 0xFB, 0xC0, 0x18, 0x94, 0xF2, 0xE1, 0xE5, 0xE9, 0x5D],
     [0xD0, 0xDC, 0x11, 0x66, 0x64, 0x5C, 0xEC, 0x59, 0x42, 0x75, 0x12, 0xF5, 0x74, 0x9C, 0xAA, 0x23],
     [0x0E, 0x86, 0xAB, 0xBE, 0x2A, 0x02, 0xE7, 0x67, 0xE6, 0x44, 0xA2, 0x6C, 0xC2, 0x93, 0x9F, 0xF1],
     [0xF6, 0xFA, 0x36, 0xD2, 0x50, 0x68, 0x9E, 0x62, 0x71, 0x15, 0x3D, 0xD6, 0x40, 0xC4, 0xE2, 0x0F],
     [0x8E, 0x83, 0x77, 0x6B, 0x25, 0x05, 0x3F, 0x0C, 0x30, 0xEA, 0x70, 0xB7, 0xA1, 0xE8, 0xA9, 0x65],
     [0x8D, 0x27, 0x1A, 0xDB, 0x81, 0xB3, 0xA0, 0xF4, 0x45, 0x7A, 0x19, 0xDF, 0xEE, 0x78, 0x34, 0x60]]

S1 = [[0x55, 0xC2, 0x63, 0x71, 0x3B, 0xC8, 0x47, 0x86, 0x9F, 0x3C, 0xDA, 0x5B, 0x29, 0xAA, 0xFD, 0x77],
      [0x8C, 0xC5, 0x94, 0x0C, 0xA6, 0x1A, 0x13, 0x00, 0xE3, 0xA8, 0x16, 0x72, 0x40, 0xF9, 0xF8, 0x42],
      [0x44, 0x26, 0x68, 0x96, 0x81, 0xD9, 0x45, 0x3E, 0x10, 0x76, 0xC6, 0xA7, 0x8B, 0x39, 0x43, 0xE1],
      [0x3A, 0xB5, 0x56, 0x2A, 0xC0, 0x6D, 0xB3, 0x05, 0x22, 0x66, 0xBF, 0xDC, 0x0B, 0xFA, 0x62, 0x48],
      [0xDD, 0x20, 0x11, 0x06, 0x36, 0xC9, 0xC1, 0xCF, 0xF6, 0x27, 0x52, 0xBB, 0x69, 0xF5, 0xD4, 0x87],
      [0x7F, 0x84, 0x4C, 0xD2, 0x9C, 0x57, 0xA4, 0xBC, 0x4F, 0x9A, 0xDF, 0xFE, 0xD6, 0x8D, 0x7A, 0xEB],
      [0x2B, 0x53, 0xD8, 0x5C, 0xA1, 0x14, 0x17, 0xFB, 0x23, 0xD5, 0x7D, 0x30, 0x67, 0x73, 0x08, 0x09],
      [0xEE, 0xB7, 0x70, 0x3F, 0x61, 0xB2, 0x19, 0x8E, 0x4E, 0xE5, 0x4B, 0x93, 0x8F, 0x5D, 0xDB, 0xA9],
      [0xAD, 0xF1, 0xAE, 0x2E, 0xCB, 0x0D, 0xFC, 0xF4, 0x2D, 0x46, 0x6E, 0x1D, 0x97, 0xE8, 0xD1, 0xE9],
      [0x4D, 0x37, 0xA5, 0x75, 0x5E, 0x83, 0x9E, 0xAB, 0x82, 0x9D, 0xB9, 0x1C, 0xE0, 0xCD, 0x49, 0x89],
      [0x01, 0xB6, 0xBD, 0x58, 0x24, 0xA2, 0x5F, 0x38, 0x78, 0x99, 0x15, 0x90, 0x50, 0xB8, 0x95, 0xE4],
      [0xD0, 0x91, 0xC7, 0xCE, 0xED, 0x0F, 0xB4, 0x6F, 0xA0, 0xCC, 0xF0, 0x02, 0x4A, 0x79, 0xC3, 0xDE],
      [0xA3, 0xEF, 0xEA, 0x51, 0xE6, 0x6B, 0x18, 0xEC, 0x1B, 0x2C, 0x80, 0xF7, 0x74, 0xE7, 0xFF, 0x21],
      [0x5A, 0x6A, 0x54, 0x1E, 0x41, 0x31, 0x92, 0x35, 0xC4, 0x33, 0x07, 0x0A, 0xBA, 0x7E, 0x0E, 0x34],
      [0x88, 0xB1, 0x98, 0x7C, 0xF3, 0x3D, 0x60, 0x6C, 0x7B, 0xCA, 0xD3, 0x1F, 0x32, 0x65, 0x04, 0x28],
      [0x64, 0xBE, 0x85, 0x9B, 0x2F, 0x59, 0x8A, 0xD7, 0xB0, 0x25, 0xAC, 0xAF, 0x12, 0x03, 0xE2, 0xF2]]


def int2list(aInt, n):
    """
    将一个整型转为列表，存储其二进制比特位
    :param aInt: 整型数
    :param n: 二进制数的比特位数
    :return: 列表存储的二进制数
    """
    listValue = []
    for i in range(n):
        listValue.append((aInt >> (n - 1 - i)) & 0b1)
    return listValue


def list2int(aList, n):
    """
    将一个用列表存储的二进制数转为整型
    :param aList: 列表存储的二进制数
    :param n: 二进制数的比特位数
    :return: 整型的二进制数
    """
    intValue = 0
    for i in range(n):
        intValue = (intValue << 1) + aList[i]
    return intValue


def initialize(origKey, origIV):
    """
    初始化阶段
    :param origKey: 128bit初始密钥（整型存储）
    :param origIV: 128bit初始向量（整型存储）
    :return: 返回寄存器单元变量数组s
    """
    # 所有量转为列表存储
    origKey_list = int2list(origKey, 128)
    origIV_list = int2list(origIV, 128)
    d_list = []
    for i in range(16):
        d_list.append(int2list(D[i], 15))

    # 构造s
    s = 16 * [[]]
    for i in range(16):
        s[i] = copy.deepcopy(origKey_list[(i * 8):((i + 1) * 8)] + d_list[i] + origIV_list[(i * 8):((i + 1) * 8)])
    return s


def bitReconstruction(s):
    """
    比特重组BR，从LFSR的寄存器单元中抽取128bit，组成4个32bit字X0 X1 X2 X3
    :param s: LFSR的寄存器单元（列表存储）
    :return: 4个32bit字X0 X1 X2 X3（列表存储）
    """

    X0 = s[15][0:16] + s[14][15:31]
    X1 = s[11][15:31] + s[9][0:16]
    X2 = s[7][15:31] + s[5][0:16]
    X3 = s[2][15:31] + s[0][0:16]

    return X0, X1, X2, X3


def L(X, flag):
    """
    32bit线性L变换L1或L2
    :param X: 32bit输入（列表存储）
    :param flag: 标识符，flag指定是L1变换还是L2变换
    :return: 32比特L变换后数据（整型存储）
    """
    if flag == 1:
        tmp1 = list2int(X[2:32] + X[0:2], 32)
        tmp2 = list2int(X[10:32] + X[0:10], 32)
        tmp3 = list2int(X[18:32] + X[0:18], 32)
        tmp4 = list2int(X[24:32] + X[0:24], 32)
        return list2int(X, 32) ^ tmp1 ^ tmp2 ^ tmp3 ^ tmp4
    elif flag == 2:
        tmp1 = list2int(X[8:32] + X[0:8], 32)
        tmp2 = list2int(X[14:32] + X[0:14], 32)
        tmp3 = list2int(X[22:32] + X[0:22], 32)
        tmp4 = list2int(X[30:32] + X[0:30], 32)
        return list2int(X, 32) ^ tmp1 ^ tmp2 ^ tmp3 ^ tmp4


def SBOX(after_L):
    """
    S盒变换
    :param after_L: L变换后的32bit数据（整型存储）
    :return: 32bitSBOX变换后数据（整型存储）
    """
    res = 0
    for i in range(4):
        # 分理出x和y
        x = ((after_L >> ((3 - i) * 8)) >> 4) & 0xF
        y = (after_L >> ((3 - i) * 8)) & 0xF
        if i == 0 or i == 2:
            res = (res << 8) + S0[x][y]
        elif i == 1 or i == 3:
            res = (res << 8) + S1[x][y]
    return res


def F(X0, X1, X2, R1, R2):
    """
    非线性函数F
    :param X0: 32比特字X0（列表存储）
    :param X1: 32比特字X1（列表存储）
    :param X2: 32比特字X2（列表存储）
    :param R1: 32bit记忆单元变量R1（整型存储）
    :param R2: 32bit记忆单元变量R2（整型存储）
    :return: 32比特字W，以及更新的R1和R2（整型存储）
    """
    # 将列表存储的二进制数转为整型
    X0_int = list2int(X0, 32)
    X1_int = list2int(X1, 32)
    X2_int = list2int(X2, 32)

    W = ((X0_int ^ R1) + R2) % 0x100000000  # 模2^32加法
    W1 = (R1 + X1_int) % 0x100000000
    W2 = (R2 ^ X2_int)

    after_L1 = L((int2list(W1, 32)[16:32] + int2list(W2, 32)[0:16]), 1)
    R1 = SBOX(after_L1)
    after_L2 = L((int2list(W2, 32)[16:32] + int2list(W1, 32)[0:16]), 2)
    R2 = SBOX(after_L2)

    return W, R1, R2


def LFSR_initialisationMode(u, s):
    """
    初始化模式下的线性反馈移位寄存器LFSR
    :param u: 由非线性函数F的32bit输出W舍弃最低位得到（整型存储）
    :param s: 16个31bit寄存器单元变量（列表存储）
    :return: 更新的s（列表存储）
    """
    tmp1 = list2int(s[15], 31)
    tmp2 = list2int(s[13], 31)
    tmp3 = list2int(s[10], 31)
    tmp4 = list2int(s[4], 31)
    tmp5 = list2int(s[0], 31)
    v = (0x8000 * tmp1 + 0x20000 * tmp2 + 0x200000 * tmp3 +
         0x100000 * tmp4 + (1 + 0x100) * tmp5) % 0x7FFFFFFF  # 模2^31-1

    s_16 = (v + u) % 0x7FFFFFFF
    if s_16 == 0:
        s_16 = 0x7FFFFFFF

    for i in range(15):
        s[i] = copy.deepcopy(s[i + 1])
    s[15] = copy.deepcopy(int2list(s_16, 31))

    return s


def LFSR_workMode(s):
    """
    工作模式下的线性反馈移位寄存器LFSR
    :param s: 16个31bit寄存器单元变量（列表存储）
    :return: 更新的s（列表存储）
    """
    tmp1 = list2int(s[15], 31)
    tmp2 = list2int(s[13], 31)
    tmp3 = list2int(s[10], 31)
    tmp4 = list2int(s[4], 31)
    tmp5 = list2int(s[0], 31)
    s_16 = (0x8000 * tmp1 + 0x20000 * tmp2 + 0x200000 * tmp3 +
            0x100000 * tmp4 + (1 + 0x100) * tmp5) % 0x7FFFFFFF  # 模2^31-1

    if s_16 == 0:
        s_16 = 0x7FFFFFFF

    for i in range(15):
        s[i] = copy.deepcopy(s[i + 1])
    s[15] = copy.deepcopy(int2list(s_16, 31))

    return s


def ZUC_128(origKey, origIV, num):
    """
    ZUC-128算法
    :param origKey: 初始密钥（整型存储）
    :param origIV: 初始IV（整型存储）
    :param num: 工作阶段密钥输出节拍数
    :return: 无，随运算过程的每个节拍输出32bit密钥字Z
    """
    # 初始化阶段
    s = initialize(origKey, origIV)
    R1, R2 = 0, 0
    for i in range(32):
        X0, X1, X2, X3 = bitReconstruction(s)
        W, R1, R2 = F(X0, X1, X2, R1, R2)
        s = copy.deepcopy(LFSR_initialisationMode(W >> 1, s))

    # 工作阶段
    X0, X1, X2, X3 = bitReconstruction(s)
    W, R1, R2 = F(X0, X1, X2, R1, R2)
    s = copy.deepcopy(LFSR_workMode(s))
    # 密钥输出阶段
    for i in range(num):
        X0, X1, X2, X3 = bitReconstruction(s)
        W, R1, R2 = F(X0, X1, X2, R1, R2)
        Z = W ^ list2int(X3, 32)
        print(hex(Z))
        s = copy.deepcopy(LFSR_workMode(s))


if __name__ == "__main__":
    print("--------ZUC_128--------")
    # origKey = eval(input("请输入128bit初始密钥（16进制）："))
    # origIV = eval(input("请输入128bit初始向量（16进制）："))
    # num = eval(input("请输入密钥输出的节拍数："))
    num = 5

    print("\ntest1:")
    origKey = 0x00000000000000000000000000000000
    origIV = 0x00000000000000000000000000000000
    ZUC_128(origKey, origIV, num)

    print("\ntest2:")
    origKey = 0xffffffffffffffffffffffffffffffff
    origIV = 0xffffffffffffffffffffffffffffffff
    ZUC_128(origKey, origIV, num)

    print("\ntest3:")
    origKey = 0x3d4c4be96a82fdaeb58f641db17b455b
    origIV = 0x84319aa8de6915ca1f6bda6bfbd8c766
    ZUC_128(origKey, origIV, num)
