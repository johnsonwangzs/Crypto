import random
if __name__ == '__main__':
    fout = open("testHexTxt.txt", "wb")
    N = 5
    for i in range(N):
        for j in range(16):
            a = random.randint(0, 255)
            fout.write(int(a).to_bytes(length=1, byteorder='little', signed=False))
    for i in range(16):
        fout.write(int(16).to_bytes(length=1, byteorder='little', signed=False))
    fout.close()