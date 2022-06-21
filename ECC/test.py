import random


def genText():
    fout = open("testin", "wb")
    PC = 2
    fout.write(int(PC).to_bytes(length=1, byteorder='little', signed=False))

    S = "abcdefghijklmnopqrstuvwxyz123456"
    for i in range(len(S)):
        fout.write(ord(S[i]).to_bytes(length=1, byteorder='little', signed=False))

    fout.close()


if __name__ == "__main__":
    # genText()
    a = [1, 0, 1, 1]
    b = [23, 54]
    s = 0
    for num in a + b:
        s += num
    print(s)
