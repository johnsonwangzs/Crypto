import Add as add
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def divide(a, b):  # 求商，其中a为被除数，b为除数
    len_a = a.bit_length()
    len_b = b.bit_length()
    len_dif = len_a - len_b + 1  # a和b二进制长度之差

    if len_dif < 1:  # 如果两个多项式被除数比除数的次数低
        return 0, a  # 商为0，余数为a
    elif len_dif == 1:  # 如果两个多项式同次数
        return 1, add.addorMinus(a, b)  # 商为1，余数为a、b之差
    else:
        quotient = 0
        while len_a >= len_b:
            b1 = b << (len_a - len_b)  # b1的长度与a相等
            a = add.addorMinus(a, b1)  # a与b1作差
            quotient ^= (1 << (len_a - len_b))  # 商
            len_a = a.bit_length()  # a的新长度
        return quotient, a  # 余数为最后退出循环的a


if __name__ == '__main__':
    # a = eval(input("Please input a = "))
    # b = eval(input("Please input b = "))
    graphviz = GraphvizOutput()
    graphviz.output_file = 'Divide.png'
    with PyCallGraph(output=graphviz):
        a = 0xde
        b = 0xc6
        quotient, remainder = divide(a, b)
        print("a/b = {}...{}".format(hex(quotient), hex(remainder)))
        a = 0x8c
        b = 0x0a
        quotient, remainder = divide(a, b)
        print("a/b = {}...{}".format(hex(quotient), hex(remainder)))
        a = 0x3e
        b = 0xa4
        quotient, remainder = divide(a, b)
        print("a/b = {}...{}".format(hex(quotient), hex(remainder)))
