from function import extended_GCD as exGCD


class Point:
    """
    点的类
    """
    def __init__(self):
        self.x = None  # x坐标
        self.y = None  # y坐标


def add(P, Q, p, a):
    """
    ECC加法运算：约定用Zp中不可能出现的坐标值(0,0)表示无穷远点O
    :param P: 椭圆曲线上的一个点
    :param Q: 椭圆曲线上的另一个点
    :param p: 定义在Zp上的素曲线使用的模p
    :param a: 用来定义曲线的一个参数
    :return: 椭圆曲线上两点的加法结果R
    """

    R = Point()

    if P.x == 0 and P.y == 0:  # 其中一点是无穷远点O的情况
        return Q
    if Q.x == 0 and Q.y == 0:
        return P

    if P.x == Q.x and P.y + Q.y == p:  # P=-Q时
        O = Point()
        O.x, O.y = 0, 0
        return O

    if P.x == Q.x and P.y == Q.y:  # P=Q时
        lamb = (((3 * P.x * P.x + a) % p) * exGCD.extended_gcd(2 * P.y, p)[1]) % p
    else:
        lamb = (((Q.y - P.y) % p) * exGCD.extended_gcd(Q.x - P.x, p)[1]) % p

    R.x = (lamb * lamb - P.x - Q.x) % p
    R.y = (lamb * (P.x - R.x) - P.y) % p

    return R


def neg_P(P, p):
    """
    给定点P，输出-P
    :param P: 一个点
    :param p: 定义在Zp上的素曲线使用的模p
    :return: 一个点-P
    """
    nP = Point()
    nP.x = P.x
    nP.y = p - P.y
    return nP


def multiply(P, n, p, a):
    """
    ECC乘法运算：约定用Zp中不可能出现的坐标值(0,0)表示无穷远点O
    :param P: 椭圆曲线上的一个点
    :param n: 乘法的系数
    :param p: 定义在Zp上的素曲线使用的模p
    :param a: 用来定义曲线的一个参数
    :return: 椭圆曲线上一点的乘法结果res
    """
    res = Point()
    res.x, res.y = 0, 0  # 初始化为无穷远点O

    for i in range(n):
        res = add(res, P, p, a)

    print(res.x, res.y)
    return res


def fast_multiply(P, n, p, a):
    """
    仿照快速模幂算法优化的ECC乘法运算
    :param P: 椭圆曲线上的一个点
    :param n: 乘法的系数
    :param p: 定义在Zp上的素曲线使用的模p
    :param a: 用来定义曲线的一个参数
    :return: 椭圆曲线上一点的乘法结果res
    """
    res = Point()
    res.x, res.y = 0, 0
    while n > 0:
        if n % 2 == 1:
            res = add(res, P, p, a)
            n = (n - 1) // 2
        else:
            n = n // 2
        P = add(P, P, p, a)
    # print(res.x, res.y)
    return res


if __name__ == "__main__":
    G = Point()
    G.x, G.y = 2, 2
    multiply(G, 240, 211, 0)
    fast_multiply(G, 240, 211, 0)
    fast_multiply(G, 4, 257, 0)
