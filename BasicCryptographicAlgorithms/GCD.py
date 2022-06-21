def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def main():
    a = eval(input("Please input a: "))
    b = eval(input("Please input b: "))
    print("gcd({0},{1}) = {2}".format(a, b, gcd(a, b)))


if __name__ == '__main__':
    main()
