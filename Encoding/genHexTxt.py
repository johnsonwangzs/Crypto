import random
if __name__ == '__main__':
    fout = open("testHexTxt.txt", "wb")
    N = 5
    a = random.randint(0, 255)
    for i in range(N):
        for j in range(16):
            fout.write(int(a).to_bytes(length=1, byteorder='little', signed=False))
    fout.close()
