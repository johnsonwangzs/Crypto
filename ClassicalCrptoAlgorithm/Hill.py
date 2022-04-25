# Hill密码
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
R = []
R_js = 0


def encrypt(m, order, key_matrix):
    i = 0
    c = []
    while i < len(m):
        m1 = list(m[i: i + order])  # 明文切片，依次加密
        for j in range(order):
            m1[j] = (ord(m1[j]) - 97) % 26
        # 矩阵乘法
        for j in range(order):  # 对应密钥矩阵列数
            s = 0
            for k in range(order):  # 对应密钥矩阵行数
                s += m1[k] * key_matrix[k][j]
            s %= 26
            c.append(s)
        i += order
    for i in range(len(m)):
        c[i] = chr(c[i] + 97)
    return ''.join(c)


def AllRange(listx, start, end):  # 全排列
    global R, R_js
    if start == end:
        R.append([])
        for i in listx:
            R[R_js].append(i)
        R_js += 1
    for m in range(start, end + 1):
        listx[m], listx[start] = listx[start], listx[m]
        AllRange(listx, start + 1, end)
        listx[m], listx[start] = listx[start], listx[m]


def reverse_cnt(p, n):  # 计算n个数的序列p的逆序数
    js = 0  # 逆序数
    for i in range(n - 1):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                js += 1
    return js


def det(matrix, order):  # 使用定义法计算order阶行列式matrix的值
    # 首先计算0到order-1的全排列，以子列表的形式保存在列表R中
    global R, R_js
    R = []
    R_js = 0
    list1 = []
    for i in range(order):
        list1.append(i)
    AllRange(list1, 0, order - 1)
    # 根据js=order!个全排列序列来计算det(matrix)
    d = 0
    for i in range(R_js):
        m = 1  # 行列式求值
        t = reverse_cnt(R[i], order)  # 对某个特定的序列R[i]，求逆序数
        for j in range(order):
            m *= matrix[j][R[i][j]]
        d += pow(-1, t) * m
    return d


def cal_M(matrix, order, x, y):  # 计算order阶矩阵matrix中(x,y)位置元素的余子式
    M = []  # 余子式（矩阵）
    js = 0
    for i in range(order):
        if i != x:
            M.append([])
            for j in range(order):
                if j != y:
                    M[js].append(matrix[i][j])
            js += 1
    m = det(M, order - 1)  # 余子式（行列式）
    return m


def multi_inverse(a, b):  # extended_gcd求逆元
    if b == 0:
        return a, 1, 0
    else:
        gcd, xtmp, ytmp = multi_inverse(b, a % b)
        x = ytmp
        y = xtmp - int(a // b) * ytmp
        return gcd, x, y


def inverse_matrix(matrix, order):  # 求逆矩阵
    matrix_inv = []
    A = []  # matrix的伴随矩阵的转置
    # 先求伴随矩阵的转置
    for i in range(order):
        A.append([])
        for j in range(order):
            M = cal_M(matrix, order, i, j)  # 余子式
            a = pow(-1, i + j) * M  # 代数余子式
            A[i].append(a)
    # 求伴随矩阵A1（由A转置得）
    A1 = []
    for i in range(order):
        A1.append([])
        for j in range(order):
            A1[i].append(A[j][i])
    # 求行列式
    d = det(matrix, order) % 26
    tmp1, e, tmp2 = multi_inverse(d, 26)  # 行列式关于模26的逆元
    # 求最终逆矩阵
    for i in range(order):
        matrix_inv.append([])
        for j in range(order):
            matrix_inv[i].append(A1[i][j] * e % 26)
    return matrix_inv


def decrypt(c, order, key_matrix):
    i = 0
    m = []
    key_matrix_inv = inverse_matrix(key_matrix, order)
    while i < len(c):
        c1 = list(c[i: i + order])
        for j in range(order):
            c1[j] = (ord(c1[j]) - 97) % 26
        for j in range(order):
            s = 0
            for k in range(order):
                s += c1[k] * key_matrix_inv[k][j]
            s %= 26
            m.append(s)
        i += order
    for i in range(len(c)):
        m[i] = chr(m[i] + 97)
    return ''.join(m)


if __name__ == '__main__':
    print("--------Hill密码--------")
    print("模式：1=加密（输入为明文m） 2=解密（输入为密文c）。")
    mode = eval(input("输入模式mode："))
    order = eval(input("输入密钥矩阵的阶数order："))
    key_matrix = []
    print("--接下来输入密钥矩阵，分{0}行输入，每行{0}个数，用空格分隔。每行输入完后回车换行--".format(order))
    for i in range(order):  # 输入n阶矩阵
        key_matrix.append([])
        key_matrix[i] = input("输入密钥矩阵第{}行（用空格分隔）：".format(i + 1)).split(' ')
        for j in range(order):
            key_matrix[i][j] = int(key_matrix[i][j])
    if mode == 1:
        m = input("请输入要加密的明文串m：")
        c = encrypt(m, order, key_matrix)
        print("加密后密文c为：", c)
    elif mode == 2:
        c = input("请输入要解密的密文串c：")
        m = decrypt(c, order, key_matrix)
        print("解密后明文m为：", m)

    # graphviz = GraphvizOutput()
    # graphviz.output_file = 'Hill.png'
    # with PyCallGraph(output=graphviz):
    #     key_matrix = [[17, 17, 5], [21, 18, 21], [2, 2, 19]]
    #     m = "paymoremoney"
    #     c = encrypt(m, 3, key_matrix)
    #     print("\n加密paymoremoney\n-->{}".format(c))
    #     c = "rrlmwbkaspdh"
    #     m = decrypt(c, 3, key_matrix)
    #     print("\n解密rrlmwbkaspdh\n-->{}".format(m))
    #
    #     key_matrix = [[5, 8], [17, 3]]
    #     m = "loveyourself"
    #     c = encrypt(m, 2, key_matrix)
    #     print("\n加密loveyourself\n-->{}".format(c))
    #
    #     key_matrix = [[6, 24, 1], [13, 16,10], [20, 17, 15]]
    #     c = "qweasdzxc"
    #     m = decrypt(c, 3, key_matrix)
    #     print("\n解密qweasdzxc\n-->{}".format(m))

