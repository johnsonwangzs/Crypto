"""
    Description: m维 Hill密码 (明文左乘矩阵)的已知明文攻击；
"""
import Hill
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

availableDet = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
m_chosen_ch = []
m_chosen_pos = []


def check_isInv(m, order, choose_ch, choose_pos, used):  # 全排列查找合适的明文矩阵（需可逆）
    global m_chosen_ch, m_chosen_pos
    if len(choose_ch) == order:  # 若已经选择的明文字符分组数达到形成矩阵所需的个数
        tmp = []
        for i in range(order):
            tmp.append(choose_ch[i])
        d = Hill.det(tmp, order) % 26  # 计算行列式
        if d in availableDet:  # 若d是符合条件的行列式值，则返回这个合格的明文矩阵
            m_chosen_ch = tmp
            m_chosen_pos = choose_pos
            return tmp, used
        else:
            return [], []
    else:
        for i in range(len(m)):
            if used[i] == 1:
                continue
            choose_ch.append(m[i])
            choose_pos.append(i)
            used[i] = 1
            ans = check_isInv(m, order, choose_ch, choose_pos, used)
            if ans != ([], []):
                return ans, used
            choose_ch.pop()
            choose_pos.pop()
            used[i] = 0
        return [], []


def attackHill(m, c, order):
    global m_chosen_ch, m_chosen_pos
    m_chosen_ch = []
    m_chosen_pos = []
    # 对明文进行分组
    m_group = []
    tmp = []
    for i in range(len(m)):
        tmp.append(ord(m[i]) - 97)
        if len(tmp) == order:
            m_group.append(tmp)
            tmp = []
    # 求合适的明文矩阵（可逆）
    check_isInv(m_group, order, [], [], [0 for i in range(len(m_group))])  # chosen为最终选中为矩阵元素的明文字符分组
    if m_chosen_ch == []:
        print("此例不可求得！")
        return
    else:
        mMatrix = m_chosen_ch  # 找到合适的明文矩阵！
        # 求明文矩阵的逆矩阵
        mMatrix_inv = Hill.inverse_matrix(mMatrix, order)
        # 对密文进行分组
        c_group = []
        tmp = []
        for i in range(len(c)):
            tmp.append(ord(c[i]) - 97)
            if len(tmp) == order:
                c_group.append(tmp)
                tmp = []
        cMatrix = []  # 密文矩阵
        for i in range(order):
            cMatrix.append(c_group[m_chosen_pos[i]])
        # 明文矩阵的逆矩阵 与 密文矩阵 进行矩阵乘法运算，求解密钥矩阵
        kMatrix = []
        for i in range(order):
            kMatrix.append([])
            for j in range(order):
                s = 0
                for k in range(order):
                    s += mMatrix_inv[i][k] * cMatrix[k][j]
                kMatrix[i].append(s % 26)
        return kMatrix


if __name__ == '__main__':
    print("--------Hill密码（已知明文）攻击--------")
    order = eval(input("输入密钥矩阵的维度order："))
    m = input("请输入已知的明文：")
    c = input("请输入已知明文加密后的密文：")
    keyMatrix = attackHill(m, c, order)
    print("密钥矩阵为：", keyMatrix)

    # graphviz = GraphvizOutput()
    # graphviz.output_file = 'Hill_attack.png'
    # with PyCallGraph(output=graphviz):
    #     print("attack1-->")
    #     print("密钥：", attackHill("youarepretty", "kqoimjvdbokn", 2))
    #     print()
    #     print("attack2-->")
    #     print("密钥：", attackHill("youaresocute", "ywwpcwsogfuk", 3))
