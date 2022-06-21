import ExEuclid as eE
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def multi_inverse(a, m):
    tmp1, e, tmp2 = eE.exEuclid(a, m, m)
    return e


if __name__ == '__main__':
    m = 0b100011011
