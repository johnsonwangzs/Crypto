import math
import RSA
from Power_module_FAST import *
from SHA1 import *
from BBS import *
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

sLen = 20  # 盐的字节长度 一般sLen=hLen，当前版本为20字节
hLen = 20  # hash函数值的字节长度 这里取SHA-1，160bit即20字节
emBits = 512


def genSalt():
    """
    生成盐（一组伪随机数，长为sLen字节）
    :return: 盐
    """
    # 调用BBS伪随机数算法生成一个伪随机01比特串
    salt_bit = BBS(sLen * 8)
    while len(salt_bit) != 160:
        salt_bit = BBS(sLen * 8)

    # 将比特串转为字节串
    salt_byte, aByte = b'', 0
    for i in range(len(salt_bit)):
        aByte = (aByte << 1) + salt_bit[i]
        if i % 8 == 7:
            salt_byte = salt_byte + aByte.to_bytes(1, byteorder='big')
            aByte = 0

    # salt = 0xfa4b050986101331d18cd00df3bf6cddd3a2fa14
    # salt_byte = salt.to_bytes(20, byteorder='big')
    return salt_byte


def MGF(X, maskLen):
    """
    掩码生成函数MGF1，用于产生任意长度消息的摘要或者hash值，输出固定长度的值
    :param X: M'即M_pad_byte的hash值（字节串）
    :param maskLen: 掩码长度=emLen-hLen-1
    :return: mask=T的前maskLen字节
    """
    global hLen

    T = b''
    k = math.ceil(maskLen / hLen) - 1

    for counter in range(0, k + 1):
        C = counter.to_bytes(4, byteorder='big')
        T = T + SHA1(X + C).to_bytes(20, byteorder='big')

    mask = b''
    mask = T[:maskLen]
    return mask


def bytes2int(aBytes):
    """
    字节串转整数
    :param aBytes: 一个字节串
    :return: 转换后的整数
    """
    result = 0
    for i in range(0, len(aBytes)):
        result = (result << 8) + aBytes[i]
    return result


def msgEncode(msg):
    """
    消息编码函数
    :param msg: 消息（字符串）
    :return: 编码后消息EM
    """
    global emBits, hLen
    msg_byte = msg.encode()  # 消息由字符串转为字节串
    mHash = SHA1(msg_byte)
    mHash_byte = mHash.to_bytes(hLen, byteorder='big')  # 由整型转为字节

    salt_byte = genSalt()  # 求盐
    print("salt:", hex(bytes2int(salt_byte)))
    M_pad_byte = int(0x00).to_bytes(1, byteorder='big') * 8 + mHash_byte + salt_byte  # 填充1、盐，构造M‘
    print("M':", hex(bytes2int(M_pad_byte)))

    H = SHA1(M_pad_byte)  # H=hash(M')
    print("H:", hex(H))
    emLen = math.ceil(emBits / 8)
    DB_byte = int(0x00).to_bytes(1, byteorder='big') * (emLen - sLen - hLen - 3) + int(0x01).to_bytes(1, byteorder='big') + salt_byte  # 填充2
    H_byte = H.to_bytes(20, byteorder='big')
    DBmask_byte = MGF(H_byte, emLen - hLen - 1)  # 求DBmask

    DB = bytes2int(DB_byte)
    DBmask = bytes2int(DBmask_byte)
    maskedDB = DB ^ DBmask  # 求maskedDB
    maskedDB_byte = maskedDB.to_bytes(max(len(DB_byte), len(DBmask_byte)), byteorder='big')
    maskedDB_byte = chr(0x00).encode() * ((8 * emLen - emBits) // 8) + maskedDB_byte[(8 * emLen - emBits) // 8:]

    EM_byte = maskedDB_byte + H_byte + int(0xbc).to_bytes(1, byteorder='big')  # 求消息摘要
    print("EM_byte:", EM_byte)

    return EM_byte


def sign(m, d, N):
    """
    拥有私钥和公钥的签名者进行签名
    :param m: 消息摘要（字节串）
    :param d: 签名者的私钥
    :param N: RSA中的模数N
    :return: 签名结果sig
    """
    """
    p：大质数
    q：大质数
    N=p*q：模数
    e：公钥
    d：私钥
    """
    sig = fast_pow_mod(m, d, N)
    return sig


def verify(sig, e, N, pt):
    """
    签名验证函数
    :param sig: 签名
    :param e: 验签者的公钥
    :param N: RSA的模数N
    :param pt: 明文（用于验证的消息）
    :return: 签名验证结果
    """
    # 解密
    m = fast_pow_mod(sig, e, N)  # 将签名sig解密后得到消息摘要m

    # EM验证
    tmp, modBits = N, 0  # 模数N的位长度
    while tmp > 0:
        modBits += 1
        tmp >>= 1
    emLen = math.ceil(emBits / 8)  # m转换为编码后的EM形式时的长度
    EM_byte = m.to_bytes(emLen, byteorder='big')

    pt_byte = pt.encode()
    mHash = SHA1(pt_byte)
    mHash_byte = mHash.to_bytes(20, byteorder='big')

    if emLen < hLen + sLen + 2:
        print("消息摘要EM的长度不一致！")
        return False

    if EM_byte[emLen - 1:emLen] != int(0xbc).to_bytes(1, byteorder='big'):
        print("消息摘要EM的最右侧字节不是BC！")
        return False

    # 求DB和H
    maskedDB_byte = EM_byte[0:emLen - hLen - 1]
    H_byte = EM_byte[emLen - hLen - 1:emLen - 1]
    if maskedDB_byte[0:(8 * emLen - emBits) // 8] != int(0x00).to_bytes(1, byteorder='big') * ((8 * emLen - emBits) // 8):
        print(maskedDB_byte[0:(8 * emLen - emBits) // 8])
        print(8 * emLen - emBits)
        print("maskedDB的最左字节中的最左8*emLen-emBits位不是全0！")
        return False

    # 求DB
    dbMask_byte = MGF(H_byte, emLen - hLen - 1)
    dbMask = bytes2int(dbMask_byte)
    maskedDB = bytes2int(maskedDB_byte)
    DB = maskedDB ^ dbMask
    DB_byte = DB.to_bytes(max(len(dbMask_byte), len(maskedDB_byte)), byteorder='big')


    # 设置DB的最左字节的最左8*emLen-emBits位为0，验证填充2
    DB_byte = int(0x00).to_bytes(1, byteorder='big') * ((8 * emLen - emBits) // 8) + DB_byte[(8 * emLen - emBits) // 8:]
    if DB_byte[:emLen - hLen - sLen - 1] != int(0x00).to_bytes(1, byteorder='big') * (emLen - sLen - hLen - 2) + int(0x01).to_bytes(1, byteorder='big'):
        print("DB的最左(emLen-hLen-sLen-1)字节不等于填充2！")
        return False

    # 将DB的最后sLen字节设为盐值
    salt_byte = DB_byte[len(DB_byte) - sLen:]

    # 构造M'数据块，H'=hash(M')
    M_pad_byte = int(0x00).to_bytes(1, byteorder='big') * 8 + mHash_byte + salt_byte
    M_pad_hash = SHA1(M_pad_byte)

    # 验证H=H'
    if H_byte == M_pad_hash.to_bytes(20, byteorder='big'):
        print("签名一致！")
        return True
    else:
        print("M'的Hash值不一致！")
        return False


def testRSA_PSS():
    """
    RSA_PSS测试函数
    :return:
    """
    # msg = input("输入待签名消息：")
    msg = "RSA-PSS数字签名"
    # 消息编码
    EM_byte = msgEncode(msg)
    EM = bytes2int(EM_byte)
    print("EM:", hex(EM))
    # RSA密钥生成
    p, q, N, e, d = RSA.key_generation()
    # 签名
    sig = sign(EM, d, N)
    print("sig:", hex(sig))
    print("----------------")
    # 验签
    vRes = verify(sig, e, N, msg)
    if vRes:
        print("签名验证成功！")
    else:
        print("签名验证失败！")


if __name__ == "__main__":
    testRSA_PSS()
