# 栅栏密码
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def encrypt(m, row):
    len_m = len(m)
    if len_m % row != 0:
        m += "*" * (row - len_m % row)  # 如果明文长度不能整除行数row，空位用*补齐
    c = ""
    for i in range(row):
        for j in range(len(m)):
            if j % row == i:  # 将明文m按照模行数row的剩余类作为区分，来对密文c依次进行填充
                c += m[j]
    return c


def decrypt(c, row):
    len_c = len(c)
    if len_c % row == 0:
        column = len_c // row
        modulus = 0
        flag = 0  # 代表余数为0
    else:
        column = len_c // row + 1
        modulus = len_c % row  # modulus：相当于最后一列有多少行，它们因len(c)不整除行数row而存在字符
        flag = 1  # 代表余数不为0

    # 例如：输入c = "0369147258"，row = 3
    # len_c = 10，则modulus=1，代表有1行在最后一列是有字符存在的：
    # 0369
    # 147
    # 258

    list_c = []
    for i in range(row):
        list_c.append([])
    i = 0
    js = 0  # 行的计数器
    while i < len_c:  # 本层循环，从第i位密文开始，依次分配到第js行所在的list中（共row行，代表每行的list[]又都是list_c[]的一个元素）
        if modulus > 0:  # modulus用来判断本行所在的list里有几个字符（因为可能密文的字符长度len_c并不整除行数row）
            for j in range(i, i + column):
                list_c[js].append(c[j])
            i += column
        else:
            for j in range(i, i + column - flag):  # 通过以上代码中的flag=0还是1来控制循环范围，
                list_c[js].append(c[j])
            i += column - flag
        modulus -= 1
        js += 1  # 本行结束，下一轮考虑下一行
    # 此时存放[['0', '3', '6', '9'], ['1', '4', '7'], ['2', '5', '8']]

    js2 = 0  # 列的计数器
    m = ""
    for i in range(len_c):
        m += list_c[i % row][js2]
        if i % row == row - 1:  # 当某一列结束，则考虑下一列
            js2 += 1
    return m


if __name__ == '__main__':
    print("--------栅栏密码--------")
    print("模式：1=加密（输入为明文m） 2=解密（输入为密文c）。")
    mode = eval(input("输入模式mode："))
    row = eval(input("输入行数row："))
    if mode == 1:
        m = input("请输入要加密的明文m：")
        c = encrypt(m, row)
        print("加密后密文c为：", c)
    elif mode == 2:
        c = input("请输入要解密的密文c：")
        m = decrypt(c, row)
        print("解密后明文m为：", m)

    # graphviz = GraphvizOutput()
    # graphviz.output_file = 'RailfenceCipher.png'
    # with PyCallGraph(output = graphviz):
    #     print("\n加密whateverisworthdoingisworthdoingwell\n-->{}".format(encrypt("whateverisworthdoingisworthdoingwell", 3)))
    #     print("\n解密hatimriprathnelhelhsoemotntawat\n-->{}".format(decrypt("hatimriprathnelhelhsoemotntawat", 2)))
