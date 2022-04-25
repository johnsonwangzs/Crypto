----------------文件----------------

----SM4及工作模式----
SM4.py：SM4加解密标准算法（128bit）
SM4_ECB.py：ECB模式下的SM4加解密
SM4_CBC.py：CBC模式下的SM4加解密
SM4_CTR.py：CTR模式下的SM4加解密

----SM4-CBC模式的PaddingOracleAttack----
oracle_SM4.py：模拟SM4解密的服务器，配合padding oracle attack使用
PaddingOracleAttack.py：padding oracle attack的攻击者使用


--------以下文件使用WinHex软件打开--------

----样例----
message：测试明文
cipher-ecb：SM4-ECB模式样例输出
cipher-cbc：SM4-CBC模式样例输出
cipher-ctr：SM4-CTR模式样例输出

----输出文件----
cipher-ecb_test：SM4-ECB模式加密程序输出
cipher-cbc_test：SM4-CBC模式加密程序输出
cipher-ctr_test：SM4-CTR模式加密程序输出
plain-ecb_test：SM4-ECB模式解密程序输出
plain-cbc_test：SM4-CBC模式解密程序输出
plain-ctr_test：SM4-CTR模式解密程序输出



----------------函数及功能----------------

----SM4----
crypt：加/解密函数
gen_key：密钥生成函数
tau：非线性变换τ
L_key：用于密钥生成的线性变换函数
T_key：用于密钥生成的T变换
L：用于加解密的线性变换函数
T：用于加解密的T变换

----模拟的SM4解密server端——解密oracle----
checkIsLegal：检验client（用户）所尝试的填充的合法性
requestDecrypt：（攻击者）向server的请求服务函数

----模拟的攻击者端----
divideCipher：攻击者对获取的密文进行拆分（每个分组128bit）
tryAttack：对某个分组的padding oracle attack攻击、还原明文
paddingAttack：对某个分组进行具体的n位填充的尝试，向解密oracle轮询以获得填充正确性的反馈







