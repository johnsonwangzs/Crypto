import extended_GCD
import gmpy2
import RSA
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from libnum import n2s


def cal_continued_fraction(curFraction):
    """
    计算渐近分数
    :param curFraction: 连分数展开中，计算当前渐近分数所需的部分
    :return: 得到的渐近分数的分母和分子
    """
    nume = 1  # 分子
    deno = 0  # 分母
    for i in range(len(curFraction) - 1, -1, -1):
        deno, nume = nume, curFraction[i] * nume + deno
    return deno, nume


def wienerAttack(e, n, ciphertext):
    """
    Wiener Attack
    :param e: 已知的公钥e
    :param n: 已知的模数N（N=p*q）
    :param c: 密文c
    :return: 明文m
    """
    # e/n的连分数展开。列表tmp保存每次展开得到的整数
    tmp = []
    x, y = e, n
    while y:
        tmp.append(x // y)
        x, y = y, x % y

    # 由连分数展开求各渐近分数
    for i in range(1, len(tmp)):
        d, k = cal_continued_fraction(tmp[0:i])  # 计算当前渐近分数
        if k == 0 or (e * d - 1) % k != 0:  # 要找的d和k需满足ed-kφ(n)=1，另外排除不合法情况
            continue

        phi_n = (e * d - 1) // k

        # 构造一元二次方程，根据判别式计算p和q
        a, b, c = 1, n - phi_n + 1, n  # 一元二次方程系数
        delta = b * b - 4 * a * c  # 由上述可得，开根号一定是整数，因为有解
        p = (-b + gmpy2.isqrt(delta)) // (2 * a)
        q = (-b - gmpy2.isqrt(delta)) // (2 * a)

        # 检验得到的p和q是否满足等式n=p*q，成立则求d
        if n == p * q:
            p, q = abs(int(p)), abs(int(q))
            tmp1, d, tmp2 = extended_GCD.extended_gcd(e, (p - 1) * (q - 1))
            m = RSA.RSA_decrypt(ciphertext, d, p, q)
            return d, p, q, m

    print("攻击失败！")


def test():
    """
    测试函数
    :return: 共计得到的私钥、大质数p和q、明文
    """
    e = 284100478693161642327695712452505468891794410301906465434604643365855064101922252698327584524956955373553355814138784402605517536436009073372339264422522610010012877243630454889127160056358637599704871937659443985644871453345576728414422489075791739731547285138648307770775155312545928721094602949588237119345
    n = 468459887279781789188886188573017406548524570309663876064881031936564733341508945283407498306248145591559137207097347130203582813352382018491852922849186827279111555223982032271701972642438224730082216672110316142528108239708171781850491578433309964093293907697072741538649347894863899103340030347858867705231
    c = 225959163039382792063969156595642930940854956840991461420767658113591137387768433807406322866630268475859008972090971902714782079518283320987088621381668841235751177056166331645627735330598686808613971994535149999753995364795142186948367218065301138932337812401877312020570951171717817363438636481898904201215
    d, p, q, m = wienerAttack(e, n, c)
    print("大质数p={0}\n大质数q={1}\n私钥sk={2}\n明文m={3}".format(p, q, d, m))
    print(n2s(m))


if __name__ == '__main__':
    test()
    # e = eval(input("请输入已知的公钥："))
    # n = eval(input("请输入已知的模数："))
    # c = eval(input("请输入要攻击的密文："))
    # d, p, q, m = wienerAttack(e, n, c)
    # print("大质数p={0}\n大质数q={1}\n私钥sk={2}\n明文m={3}".format(p, q, d, m))
