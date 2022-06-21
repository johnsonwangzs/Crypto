# GF(2^8)上的多项式乘法，假设每个多项式由一个十六/二进制数表示(8位)


def multiply(a, b, m):
    ans = 0
    while b > 0:
        if (b & 0x01) == 0x01:  # 如果b的二进制最低位为1
            ans ^= a  # 进行一次多项式乘法

        a <<= 1
        if (a & 0x100) == 0x100:  # 如果a的二进制最高位为1
            a ^= m
        a &= 0xff

        b >>= 1

    return ans


if __name__ == '__main__':
    # a = eval(input("Please input a = "))
    # b = eval(input("Please input b = "))
    m = 0b100011011
    # a = 0xce
    # b = 0xf1
    # print("a*b =", hex(multiply(a, b, m)))
    # a = 0x70
    # b = 0x99
    # print("a*b =", hex(multiply(a, b, m)))
    # a = 0x00
    # b = 0xa4
    # print("a*b =", hex(multiply(a, b, m)))
    print(hex(multiply(0x0e, 0x02, m) ^ multiply(0x0b, 0x01, m) ^ multiply(0x0d, 0x01, m) ^ multiply(0x09, 0x03, m)))
