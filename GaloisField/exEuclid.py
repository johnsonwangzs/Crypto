import Divide as div
import Add as add
import Multiply as mul


def exEuclid(a, b, m):
    if b == 0:
        return a, 1, 0
    else:
        quotient, remainder = div.divide(a, b)
        gcd, xtmp, ytmp = exEuclid(b, remainder, m)
        x = ytmp
        y = add.addorMinus(xtmp, mul.multiply(ytmp, quotient, m))
        return gcd, x, y


if __name__ == '__main__':
    # a = eval(input("Please input the value of the first poly:"))
    # b = eval(input("Please input the value of the second poly:"))
    m = 0b100011011

    a, b = 0x75, 0x35
    ans = exEuclid(a, b, m)
    gcd = ans[0]
    x = ans[1]
    y = ans[2]
    print("\nans: ({}, {}, {})".format(hex(x), hex(y), hex(gcd)))
    print("x={1}\ny={3}\n(x,y)={0}\n{0} = {1} * {2} + {3} * {4}".format(hex(gcd), hex(x), hex(a), hex(y), hex(b)))

    a, b = 0xac, 0x59
    ans = exEuclid(a, b, m)
    gcd = ans[0]
    x = ans[1]
    y = ans[2]
    print("\nans: ({}, {}, {})".format(hex(x), hex(y), hex(gcd)))
    print("x={1}\ny={3}\n(x,y)={0}\n{0} = {1} * {2} + {3} * {4}".format(hex(gcd), hex(x), hex(a), hex(y), hex(b)))

    a, b = 0xf8, 0x2e
    ans = exEuclid(a, b, m)
    gcd = ans[0]
    x = ans[1]
    y = ans[2]
    print("\nans: ({}, {}, {})".format(hex(x), hex(y), hex(gcd)))
    print("x={1}\ny={3}\n(x,y)={0}\n{0} = {1} * {2} + {3} * {4}".format(hex(gcd), hex(x), hex(a), hex(y), hex(b)))

    a, b = 0x48, 0x99
    ans = exEuclid(a, b, m)
    gcd = ans[0]
    x = ans[1]
    y = ans[2]
    print("\nans: ({}, {}, {})".format(hex(x), hex(y), hex(gcd)))
    print("x={1}\ny={3}\n(x,y)={0}\n{0} = {1} * {2} + {3} * {4}".format(hex(gcd), hex(x), hex(a), hex(y), hex(b)))
