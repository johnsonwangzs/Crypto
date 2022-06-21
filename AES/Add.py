# GF(2^8)上的多项式加法运算即为按位异或运算，减法与加法相同
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def addorMinus(a, b):
    return a ^ b  # a和b按位异或


if __name__ == '__main__':
    # a = eval(input("Please input a = "))
    # b = eval(input("Please input b = "))
    graphviz = GraphvizOutput()
    graphviz.output_file = 'Add.png'
    with PyCallGraph(output=graphviz):
        a = 0x89
        b = 0x4d
        print("a+b =", hex(addorMinus(a, b)))
        a = 0xaf
        b = 0x3b
        print("a+b =", hex(addorMinus(a, b)))
        a = 0x35
        b = 0xc6
        print("a+b =", hex(addorMinus(a, b)))
