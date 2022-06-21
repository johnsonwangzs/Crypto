--------主要代码文件--------
DES.py                   DES原算法
DES_speedTest.py         DES原算法速度测试
DES_EDE2.py              DES_EDE2算法
DES_EDE2_speedTest.py    DES_EDE2算法速度测试
AES.py                   AES原算法
AES_speedTest.py         AES原算法速度测试



--------辅助文件--------
gen_hexTxt_DES.py        生成DES算法速度测试的测试数据集
testTxt_1000.txt         DES算法速度测试的测试数据集
gen_hexTxt_AES.py        生成AES算法速度测试的测试数据集
testTxt_500.txt          AES算法速度测试的测试数据集



--------DES.py中的函数及功能--------
encrypt      DES加密函数
printInHex   16进制输出函数
IP           IP置换
genKey       轮密钥生成
F_en         加密轮函数（顺序轮密钥）
F_de         解密轮函数（逆序轮密钥）
IIP          IP逆置换
extend       扩展置换（E盒）
xorRoundKey  轮密钥加
sbox         非线性代换（S盒）
pbox         线性置换（P盒）



--------AES.py中的函数及功能--------
encrypt：DES加密函数
decrypt：DES解密函数
genKey：密钥扩展函数
T：密钥扩展中的T函数
addKey：轮密钥加函数
shiftRow：行移位函数
invShiftRow：逆向行移位函数
byteSub：字节代替函数
invByteSub：逆向字节代替函数
mixColumn：列混淆函数
invMixColumn：逆向列混淆函数
GF_multiply：GF(2^8)上的乘法运算函数
printInHex：16进制输出函数

