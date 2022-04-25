import copy

FK = \
    [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]

CK = \
    [0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
     0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
     0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
     0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
     0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
     0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
     0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
     0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]

SBOX = \
    [[0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05],
     [0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99],
     [0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62],
     [0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6],
     [0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8],
     [0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35],
     [0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87],
     [0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e],
     [0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1],
     [0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3],
     [0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f],
     [0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51],
     [0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8],
     [0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0],
     [0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84],
     [0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]]

K = []
rk = []
rk1 = []
X = []
key = 0x0123456789ABCDEFFEDCBA9876543210


def tau(A):  # 输入32bit非线性变换前数据
    a = [[], [], [], []]
    a[0] = copy.deepcopy(A[0:8])
    a[1] = copy.deepcopy(A[8:16])
    a[2] = copy.deepcopy(A[16:24])
    a[3] = copy.deepcopy(A[24:32])
    B = []
    for i in range(4):
        x, y = 0, 0
        for j in range(4):
            x = (x << 1) + a[i][j]
        for j in range(4, 8):
            y = (y << 1) + a[i][j]
        tmp = SBOX[x][y]
        for j in range(8):
            B.append((tmp >> (7 - j)) & 0b1)
    return B  # 输出32bit非线性变换后结果


def L_key(B):  # 输入32bit线性变换前数据
    B1, B2 = [], []
    B1 = copy.deepcopy(B[13:32])
    B2 = copy.deepcopy(B[23:32])
    for i in range(13):
        B1.append(B[i])
    for i in range(23):
        B2.append(B[i])
    C = []
    for i in range(32):
        C.append(B[i] ^ B1[i] ^ B2[i])
    return C  # 输出32bit线性变换后结果


def T_key(i1, i2, i3, i4):  # 密钥扩展算法中的T'变换
    global K
    # 计算K_i+1 ^ K_i+2 ^ K_i+3 ^ CK_i
    tmp = []
    for i in range(32):
        tmp.append(K[i1][i] ^ K[i2][i] ^ K[i3][i] ^ ((CK[i4] >> (31 - i)) & 0b1))
    # 非线性变换τ
    afterTau = tau(tmp)
    # 线性变换L'
    afterL_key = L_key(afterTau)
    return afterL_key


def L(B):
    B1, B2, B3, B4 = [], [], [], []
    B1 = copy.deepcopy(B[2:32])
    B2 = copy.deepcopy(B[10:32])
    B3 = copy.deepcopy(B[18:32])
    B4 = copy.deepcopy(B[24:32])
    for i in range(2):
        B1.append(B[i])
    for i in range(10):
        B2.append(B[i])
    for i in range(18):
        B3.append(B[i])
    for i in range(24):
        B4.append(B[i])
    C = []
    for i in range(32):
        C.append(B[i] ^ B1[i] ^ B2[i] ^ B3[i] ^ B4[i])
    return C


def T(i1, i2, i3, i4):
    global X
    # 计算X_i+1 ^ X_i+2 ^ X_i+3 ^ rk_i
    tmp = []
    for i in range(32):
        tmp.append(X[i1][i] ^ X[i2][i] ^ X[i3][i] ^ rk[i4][i])
    # 非线性变换τ
    afterTau = tau(tmp)
    # 线性变换L'
    afterL = L(afterTau)
    return afterL


def genKey(key):
    global K, rk1
    # 初始化MK
    MK = [[], [], [], []]
    for i in range(128):
        tmp = (key >> (127 - i)) & 0b1
        if 0 <= i <= 31:
            MK[0].append(tmp)
        elif 32 <= i <= 63:
            MK[1].append(tmp)
        elif 64 <= i <= 95:
            MK[2].append(tmp)
        elif 96 <= i <= 127:
            MK[3].append(tmp)
    # 计算Ki
    K = copy.deepcopy([])
    for i in range(4):
        K.append([])
        for j in range(32):
            K[i].append(MK[i][j] ^ ((FK[i] >> (31 - j)) & 0b1))
    # 计算rk1i
    rk1 = copy.deepcopy([])
    for i in range(32):
        rk1.append([])
        K.append([])
        afterT_key = T_key(i + 1, i + 2, i + 3, i)
        for j in range(32):
            K[i + 4].append(K[i][j] ^ afterT_key[j])
            rk1[i] = copy.deepcopy(K[i + 4])


def decrypt(txt):
    global rk, rk1, X, key
    genKey(key)
    # 若为解密，密钥反序
    rk = copy.deepcopy([])
    for i in range(32):
        rk.append([])
        rk[i] = copy.deepcopy(rk1[31 - i])
    # 初始化X
    X = copy.deepcopy([[], [], [], []])
    for i in range(128):
        tmp = (txt >> (127 - i)) & 0b1
        if 0 <= i <= 31:
            X[0].append(tmp)
        elif 32 <= i <= 63:
            X[1].append(tmp)
        elif 64 <= i <= 95:
            X[2].append(tmp)
        elif 96 <= i <= 127:
            X[3].append(tmp)
    # 进行32轮迭代
    for i in range(32):
        X.append([])
        afterT = T(i + 1, i + 2, i + 3, i)
        for j in range(32):
            X[i + 4].append(X[i][j] ^ afterT[j])
    # 最终反序变换
    res = 0
    for i in range(4):
        for j in range(32):
            res = (res << 1) + X[35 - i][j]
    return res


# 合法填充表
legalPadding = \
    [[16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
     [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
     [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
     [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
     [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
     [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
     [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
     [9, 9, 9, 9, 9, 9, 9, 9, 9],
     [8, 8, 8, 8, 8, 8, 8, 8],
     [7, 7, 7, 7, 7, 7, 7],
     [6, 6, 6, 6, 6, 6],
     [5, 5, 5, 5, 5],
     [4, 4, 4, 4],
     [3, 3, 3],
     [2, 2],
     [1]]


def checkIsLegal(afterXor):  # 检验填充是否合法
    flag = 1
    for i in range(16):
        for j in range(16 - i):
            if afterXor[j + i] != legalPadding[i][j]:
                flag = 0
                break
        if flag == 1:  # 合法
            return True
        flag = 1
    return False  # 不合法


def requestDecrypt(cipherTxt, IV):  # 攻击者提交的密文txt和IV
    midValue = decrypt(cipherTxt)
    afterXor = []
    tmp = 0
    cnt = 0
    # 计算IV和midValue的异或值
    for i in range(128):
        cnt += 1
        tmp = (tmp << 1) + ((midValue >> (127 - i)) & 0b1) ^ ((IV >> (127 - i)) & 0b1)
        if cnt == 8:
            afterXor.append(tmp)
            cnt = 0
            tmp = 0
    res = checkIsLegal(afterXor)
    if res:
        # print("# 200: (IV = {0}, cipherTxt = {1}) is legal!".format(hex(IV), hex(cipherTxt)))
        return "200"  # 合法
    else:
        # print("# 500: (IV = {0}, cipherTxt = {1}) is not legal!".format(hex(IV), hex(cipherTxt)))
        return "500"  # 不合法


if __name__ == "__main__":
    key = 0x0123456789ABCDEFFEDCBA9876543210
