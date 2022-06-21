fout1 = open("test_plaintext.txt", "wb")
x = 0x1b5e8b0f1bc78d238064826704830cdb
a = 0
for i in range(128):
    a = (a << 1) + ((x >> (127 - i)) & 0b1)
    if i % 8 == 7:
        fout1.write(int(a).to_bytes(length=1, byteorder='little', signed=False))
        a = 0

fout2 = open("test_key.txt", "wb")
x = 0x3475bd76fa040b73f521ffcd9de93f24
a = 0
for i in range(128):
    a = (a << 1) + ((x >> (127 - i)) & 0b1)
    if i % 8 == 7:
        fout2.write(int(a).to_bytes(length=1, byteorder='little', signed=False))
        a = 0