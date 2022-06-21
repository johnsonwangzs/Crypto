"""
RC4算法
"""


def KSA(k_txt):
    """
    密钥编排算法KSA
    :param k_txt: 密钥
    :return: 状态数组S
    """
    # 初始化S
    S = []
    for i in range(256):
        S.append(i)

    # 初始化T
    cnt, tmp, T = 0, [], []
    for aByte in k_txt:
        cnt += 1
        tmp.append(aByte)
    cnt1 = 0
    for i in range(256):  # 用密钥k轮转填充T
        if cnt1 == cnt:
            cnt1 = 0
        T.append(tmp[cnt1])
        cnt1 += 1

    # 用T产生S的初始置换
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        tmp1 = S[i]
        S[i] = S[j]
        S[j] = tmp1

    return S


def genKey(txt, S):
    """
    密钥生成，返回密钥列表
    :param txt: 要加密或解密的字节流
    :param S: 状态数组S
    :return: 生成的密钥列表
    """
    cnt = 0
    for aByte in txt:
        cnt += 1
    i, j, K = 0, 0, []
    while cnt > 0:
        cnt -= 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        tmp = S[i]
        S[i] = S[j]
        S[j] = tmp
        t = (S[i] + S[j]) % 256
        K.append(S[t])
    return K


def crypt(K, txt):
    """
    加密/解密，返回加解密结果
    :param K: 密钥流
    :param txt: 要加密或解密的字节流
    :return: 加解密结果
    """
    res, i = [], 0
    for aByte in txt:
        res.append(aByte ^ K[i])
        i += 1
    return res


def RC4(origtxt, key_txt, fout):
    """
    RC4算法
    :param origtxt: 原输入明（密）文
    :param key_txt: 原输入密钥
    :param fout: 输出文件
    :return: 无，随运算过程将结果输出到文件
    """
    S = KSA(key_txt)
    K = genKey(origtxt, S)
    res = crypt(K, origtxt)
    for i in res:
        fout.write(int(i).to_bytes(length=1, byteorder='little', signed=False))


if __name__ == '__main__':
    fin_txt = open("test_ciphertext.txt", "rb")
    fin_key = open("test_key.txt", "rb")
    fout = open("test_plaintext.txt", "wb")
    origtxt = fin_txt.read()
    key_txt = fin_key.read()

    RC4(origtxt, key_txt, fout)

    fin_txt.close()
    fin_key.close()
    fout.close()