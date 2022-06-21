--------文件--------
AES.py：AES加（解）密算法
genSbox：S盒（逆S盒）生成算法
exEuclid.py：GF(2^8)中的扩展欧几里得算法
multi_inverse.py：求GF(2^8)中的乘法逆元
Divide.py：GF(2^8)中的除法运算
Multiply.py：GF(2^8)中的乘法运算




--------AES函数及功能--------
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

