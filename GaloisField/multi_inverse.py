import exEuclid as eE
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def multi_inverse(a, m):
    return eE.exEuclid(a, m, m)


if __name__ == '__main__':
    # a = eval(input("Please input a:"))
    m = 0b100011011
    graphviz = GraphvizOutput()
    graphviz.output_file = 'multi_inverse.png'
    with PyCallGraph(output=graphviz):
        a = 0x8c
        temp1, e, tmp2 = multi_inverse(a, m)
        print("ans =", hex(e))
        a = 0xbe
        temp1, e, tmp2 = multi_inverse(a, m)
        print("ans =", hex(e))
        a = 0x01
        temp1, e, tmp2 = multi_inverse(a, m)
        print("ans =", hex(e))
        a = 0x95
        temp1, e, tmp2 = multi_inverse(a, m)
        print("ans =", hex(e))
