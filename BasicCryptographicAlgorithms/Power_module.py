from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def pow_mod(a, b, p):  # 计算a的b次方模p
    s = 1
    while b > 0:
        s = (s * a) % p
        b = b - 1
    return s


def main():
    base = eval(input("Please input the BASE="))
    expo = eval(input("Please input the EXPO="))
    p = eval(input("Please input the MODULUS="))

    graphviz = GraphvizOutput()
    graphviz.output_file = 'Power_module.png'
    with PyCallGraph(output=graphviz):
        print("ans =", pow_mod(base, expo, p))


if __name__ == '__main__':
    main()
