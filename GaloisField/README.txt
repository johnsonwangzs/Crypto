文件——名称及简介：
Add.py:
    GF(2^8)上的加/减运算
Multiply.py:
    GF(2^8)上的乘法运算
Divide.py:
    GF(2)上多项式的除法运算
exEuclid.py:
    GF(2^8)上的（扩展）欧几里得算法
fastpowmod.py:
    GF(2^8)的快速模幂运算
multi_inverse.py:
    GF(2^8)上的求逆元运算
primitive_poly.py:
    GF(2)上本原多项式的判定及生成


算法中包含或调用的函数——名称及作用：
addorMinus():
    多项式的加（减）法
multiply():
    多项式的乘法
divide():
    多项式的除法
fast_powmod():
    多项式的快速模幂
exEuclid():
    两个多项式进行拓展欧几里得运算
multi_inverse():
    求多项式的乘法逆元
create_poly():
    产生判断本原多项式需要用到的、形如x^n+1形式的多项式
isPrimPoly():
    判断是否为本原多项式
prim_poly():
    遍历所有8次多项式，找出不可约的
