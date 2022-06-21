import Divide as div
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def create_poly(m):
    i = 1
    x = 1
    while i <= m:
        x <<= 1
        i += 1
    x += 1
    return x


def isPrimPoly(poly):  # 判断是否为本原多项式
    i = 0x02
    flag = 1
    while i < poly:
        quotient1, remainder1 = div.divide(poly, i)
        if remainder1 == 0:  # 若余数为0，即如果能够整除某个多项式
            flag = 0
            break
        i += 1

    if flag == 1:  # 找到一个8次不可约多项式
        m = 255
        poly_m = create_poly(m)
        # poly_m = 0x8000000000000000000000000000000000000000000000000000000000000001 代表多项式poly_m = x^255 + 1
        quotient2, remainder2 = div.divide(poly_m, poly)
        if remainder2 == 0:  # 如果待检多项式poly能够整除poly_m
            n = m - 1  # 从n=254开始，poly不整除poly_n = x^n + 1
            while n > 8:
                poly_n = create_poly(n)
                quotient3, remainder3 = div.divide(poly_n, poly)
                if remainder3 == 0:  # 发现能够整除某个poly_n，则poly不是本原多项式
                    return False
                n -= 1
            return True
        else:
            return False
    else:
        return False


def prim_poly():  # 遍历所有8次多项式，找出不可约的
    poly = 0x100
    js = 0
    while poly <= 0x1ff:
        if isPrimPoly(poly):
            print(hex(poly))
            js += 1
        poly += 1
    print("Total =", js)


if __name__ == '__main__':
    print("Please enter the polynomial to be judged:\n"
          "If you only want to get all the primitive polynomials, just input -1")
    poly_judge = eval(input("input:"))

    graphviz = GraphvizOutput()
    graphviz.output_file = 'Primitive_poly.png'
    with PyCallGraph(output=graphviz):
        if poly_judge != -1:
            if isPrimPoly(poly_judge):
                print("{} is a primitive polynomial!".format(hex(poly_judge)))
            else:
                print("{} is NOT a primitive polynomial!".format(hex(poly_judge)))
        print("All of the primitive polynomials are here:")
        prim_poly()
