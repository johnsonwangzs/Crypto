import ECC_calculator as ECC_cal
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def gen_pk(q, a, gx, gy, n, na, nb):
    """
    用户A和用户B根据各自的私钥生成公钥
    :param q: 椭圆曲线参数q
    :param a: 椭圆曲线参数a
    :param gx: 基点G的x坐标
    :param gy: 基点G的y坐标
    :param n: 基点G的阶n
    :param na: 用户A的私钥na
    :param nb: 用户B的私钥nb
    :return: A的公钥pa和B的公钥pb
    """
    if n < na:
        print("用户A的私钥不合法！")
        return
    if n < nb:
        print("用户B的私钥不合法！")
        return
    G = ECC_cal.Point()
    G.x, G.y = gx, gy
    Pa = ECC_cal.fast_multiply(G, na, q, a)
    Pb = ECC_cal.fast_multiply(G, nb, q, a)
    return Pa, Pb


def checkIsSuccess(keyA, keyB):
    """
    检查keyA和keyB的一致性
    :param keyA: A计算得到的公共密钥
    :param keyB: B计算得到的公共密钥
    :return: 是否一致
    """
    if keyA.x == keyB.x and keyA.y == keyB.y:
        print("公共密钥一致，交换成功！")
    else:
        print("公共密钥不一致，交换失败！")


def get_publicKey(sk, Pk, q, a):
    """
    计算公共密钥
    :param sk:一方的私钥
    :param Pk: 另一方的公钥
    :return: 公共密钥
    """
    key = ECC_cal.fast_multiply(Pk, sk, q, a)
    return key


def DH(q, a, b, gx, gy, n, na, nb):
    """
    基于ECC的Diffie-Hellman密钥交换协议
    :param q: 椭圆曲线参数q
    :param a: 椭圆曲线参数a
    :param b: 椭圆曲线参数b
    :param gx: 基点G的x坐标
    :param gy: 基点G的y坐标
    :param n: 基点G的阶n
    :param na: 用户A的私钥na
    :param nb: 用户B的私钥nb
    :return: 无，输出交换结果
    """
    Pa, Pb = gen_pk(q, a, gx, gy, n, na, nb)
    print("A的公钥：({0},{1})".format(hex(Pa.x), hex(Pa.y)))
    print("B的公钥：({0},{1})".format(hex(Pb.x), hex(Pb.y)))
    keyA, keyB = get_publicKey(na, Pb, q, a), get_publicKey(nb, Pa, q, a)
    print("A计算得到的公共密钥：({0},{1})".format(hex(keyA.x), hex(keyA.y)))
    print("B计算得到的公共密钥：({0},{1})".format(hex(keyB.x), hex(keyB.y)))
    checkIsSuccess(keyA, keyB)


def testDH():
    q = 0x8542d69e4c044f18e8b92435bf6ff7de457283915c45517d722edb8b08f1dfc3
    a = 0x787968b4fa32c3fd2417842e73bbfeff2f3c848b6831d7e0ec65228b3937e498
    b = 0x63e4c6d3b23b0c849cf84241484bfe48f61d59a5b16ba06e6e12d1da27c5249a
    gx = 0x421debd61b62eab6746434ebc3cc315e32220b3badd50bdc4c4e6c147fedd43d
    gy = 0x0680512bcbb42c07d47349d2153b70c4e5d7fdfcbfa36ea1a85841b9e46e09a2
    n = 0x8542d69e4c044f18e8b92435bf6ff7dd297720630485628d5ae74ee7c32e79b7
    na = 0x111e32da4d217b865cccb70c847603121eae9bfd95bdf399af626d23c05c742c
    nb = 0x4f593b08c8831a5219c961e1a3406401b20655492e5000b1fb5793241501e931
    DH(q, a, b, gx, gy, n, na, nb)


if __name__ == '__main__':
    # q = eval(input("请输入椭圆曲线参数q："))
    # a = eval(input("请输入椭圆曲线参数a："))
    # b = eval(input("请输入椭圆曲线参数b："))
    # gx = eval(input("请输入基点G的x坐标："))
    # gy = eval(input("请输入基点G的y坐标："))
    # n = eval(input("请输入基点G的阶n："))
    # na = eval(input("请输入用户A的私钥na："))
    # nb = eval(input("请输入用户B的私钥nb："))
    # DH(q, a, b, gx, gy, n, na, nb)
    # DH(211, 0, -4, 2, 2, 241, 121, 203)
    testDH()
