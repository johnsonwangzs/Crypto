"""
s盒生成函数
"""
import Multi_inverse
import copy

if __name__ == '__main__':
    m = 0x11b  # 这里其实用不到这个八次不可约多项式m，但调用的有限域算法参数中有它，为简便仍使用它作为参数的填充
    # 第一步，初始化Sbox
    S = []
    for i in range(16):
        S.append([])
        for j in range(16):
            S[i].append(i * 16 + j)

    # 第二步，把S盒中的每个字节映射为它在有限域GF(2^8)中的逆
    for i in range(16):
        for j in range(16):
            if i == 0 and j == 0:
                S[i][j] = 0
            else:
                S[i][j] = copy.deepcopy(Multi_inverse.multi_inverse(S[i][j], m))

    # 第三步，对S盒中每个字节的每个位做的变换
    print("S盒：")
    c = [1, 1, 0, 0, 0, 1, 1, 0]  # 0x63的二进制位（低到高）
    for i in range(16):
        for j in range(16):
            b = []
            b_xor = 0
            for k in range(8):
                b.append((S[i][j] >> k) & 1)  # 取出S[i][j]的二进制第k位（低到高）
            for k in range(8):
                b_xor += (b[k] ^ b[(k + 4) % 8] ^ b[(k + 5) % 8] ^ b[(k + 6) % 8] ^ b[(k + 7) % 8] ^ c[k]) << k
            S[i][j] = copy.deepcopy(b_xor)
            print("0x%02X" % S[i][j], end=' ')
        print()
    print()

    print("逆S盒：")
    # 已经得到S盒，则可以直接获得逆S盒
    IS = []
    # 初始化
    for i in range(16):
        IS.append([])
        for j in range(16):
            IS[i].append(-1)
    # IS盒元素即为S盒的逆置换
    for i in range(16):
        for j in range(16):
            x = S[i][j] >> 4
            y = S[i][j] & 0b1111
            IS[x][y] = (i << 4) ^ j
    for i in range(16):
        for j in range(16):
            print("0x%02X" % IS[i][j], end=' ')
        print()
