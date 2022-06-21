from random import randint
from function.constPara import *
import DiffieHellman_origin
from function.SM2_CryptoAlgorithm import *
from function.SHA1 import SHA1
from function import RSA
import time


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


def checkIsLegal(x):
    """
    检查用户A输入私钥的合法性
    :param x: 用户A输入私钥（字符串）
    :return: 合法性
    """
    y = bytes2int(x.encode())
    if y > MAXPrKey:
        return False
    return True


if __name__ == "__main__":
    print("--------Diffie-Hellman密钥交换算法--------\n"
          "****说明****\n"
          "您是用户【A】，电脑将模拟用户【B】。\n"
          "程序将演示密钥在【A】（您）与【B】（虚拟用户）之间的交换。\n")

    PrA = input("现在请输入用户A的私钥（字符串，含英文字母、任意符号或数字）：")
    while not checkIsLegal(PrA):
        print("您输入的用户A的私钥超出ECC参数范围，请再次输入！")
        PrA = input("请输入用户A的私钥：")
    PrB = randint(1, MAXPrKey)
    print("用户B的私钥已生成（16进制）：", hex(PrB))

    print("\n下面请选择DH密钥交换方案。\n"
          "方案目录:\n"
          "No    Method\n"
          "1     原始DH交换（基于ECC）\n"
          "2     带数字签名的DH交换\n"
          "3     基于公钥证书的DH交换\n")
    method = eval(input("请输入要查看的DH密钥交换方案的编号（No)："))

    while method != -1:
        if method == 1:
            print("\n--------原始DH交换（基于ECC）--------")
            PrA_int = bytes2int(PrA.encode())
            DiffieHellman_origin.DH(PrA_int, PrB)

        elif method == 2:
            print("\n--------带数字签名的DH交换--------"
                  "\n为方便演示，假定【A】和【B】已经协商好了用一组特定的密钥，来对准备发送的key的Hash值进行加解密（详见理论作业）。"
                  "这里采用的公钥加密算法是SM2公钥加密算法。"
                  "\n以下演示【A】和【B】由一方向另一方发送密钥及其加密后的Hash值。")
            nb = 0x1649AB77_A00637BD_5E2EFE28_3FBF3535_34AA7F7C_B89463F2_08DDBC29_20BB0DA0
            G = Point()
            G.x, G.y = gx, gy
            # 【接收方】根据私钥生成公钥
            Pb = gen_pk(q, a, G, n, nb)
            print("【A】使用：({0},{1})作为公钥，对他即将发送给【B】的key的Hash值加密\n"
                  "【B】使用：{2}作为私钥，对【A】发来的key的Hash值解密。".format(Pb.x, Pb.y, nb))

            print("****发送方正在发送key及其加密后的Hash值！****")
            # 【发送方】用公钥加密消息的Hash值
            M = PrA.encode()
            mHash = SHA1(M).to_bytes(20, byteorder='big')
            C = encrypt(mHash, n, q, a, G, Pb)
            print("发送-->key：", PrA)
            print("发送-->key的Hash值加密后为（比特串）：", C)

            print("****发送方发送完毕，接收方开始接收！****")
            # 【接收方】用私钥解密消息
            res = decrypt(C, q, a, b, nb)
            print("接收<--接收方收到的key是：", PrA)
            print("接收<--接收方收到加密后key的Hash值是（比特串）：", C)
            if res != -1:
                print("对其解密得到key的Hash值：", bytes2int(res))
            else:
                print("解密错误！")
            print("接收方对key作Hash得到：", SHA1(PrA.encode()))
            print("****key的Hash值相同，key发送成功！****")

        elif method == 3:
            print("--------基于公钥证书的DH交换--------"
                  "\n【B】拿到【A】的证书，要对【A】的公开公钥：{0}进行验证。"
                  "\n证书由CA颁发。".format(PrA))

            print("****首先模拟CA颁发整数的过程。****")
            ticks = math.ceil(time.time())  # 获取当前时间戳
            CA_id = b'CA_id'
            user_A = b'user_A'
            p, q, n, PrCA, PuCA = RSA.key_generation()
            print("CA的id是：{0}\n"
                  "CA持有：{1}，并公开：{2}".format(CA_id, PrCA, PuCA))
            print("CA获取【A】的ID为{0}，"
                  "CA获取当前时间戳ticks为：{1}".format(user_A, ticks))
            m = user_A + ticks.to_bytes(8, byteorder='big') + CA_id
            m_int = bytes2int(m)
            print("CA生成(ID||ticks||CA_id)为：", m_int)
            c = RSA.RSA_encrypt(m_int, PrCA, n)
            print("CA用其密钥加密后：", c)
            print("****CA公布【A】的证书，【B】验证****")
            print("【B】用CA公开的密钥解密其证书：", RSA.RSA_decrypt(c, PuCA, p, q))
            print("****证书验证成功！****")

        print("\n--------密钥交换演示完毕！--------\n"
              "是否继续使用本私钥测试其他密钥交换方案？\n"
              "是，则请输入方案编号（No）；否，则输入-1。")
        method = eval(input())

