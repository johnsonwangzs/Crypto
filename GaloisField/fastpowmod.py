import Multiply as mul
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def fast_powmod(x, n, m):
    d = 1
    while n > 0:
        if n % 2 == 1:
            d = mul.multiply(d, x, m)
            n = (n - 1) // 2
        else:
            n = n // 2
        x = mul.multiply(x, x, m)
    return d


if __name__ == '__main__':
    # x = eval(input("Please input the value of x (the base) = "))
    # n = eval(input("Please input the value of n (the expo) = "))
    m = 0b100011011
    graphviz = GraphvizOutput()
    graphviz.output_file = 'fastpowmod.png'
    with PyCallGraph(output=graphviz):
        x, n = 0x89, 18829
        print("x^n mod m =", hex(fast_powmod(x, n, m)))
        x, n = 0x3e, 28928
        print("x^n mod m =", hex(fast_powmod(x, n, m)))
        x, n = 0x19, 26460
        print("x^n mod m =", hex(fast_powmod(x, n, m)))
        x, n = 0xba, 13563
        print("x^n mod m =", hex(fast_powmod(x, n, m)))
