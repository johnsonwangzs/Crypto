import math
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def sieve(n):
    js = 0
    flag = [1] * (n + 1)  # 初始化标记列表，初值均为1代表未筛
    i = 2
    m = int(math.sqrt(n))  # 计算根号n
    while i <= m:
        if flag[i] == 1:
            j = 2 * i
            while j <= n:
                flag[j] = 0
                j = j + i
        i = i + 1
    k = 2
    while k <= n:
        if flag[k] == 1:
            print(k)
            js = js + 1
        k = k + 1
    print("total=", js)


def main():
    #n = eval(input("please input N="))
    # n = 2
    # n = 103
    # n = 10000
    n = 1000000
    graphviz = GraphvizOutput()
    graphviz.output_file = 'eratosthenes.png'
    with PyCallGraph(output=graphviz):
        sieve(n)


if __name__ == '__main__':
    main()


