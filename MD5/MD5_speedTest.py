import MD5
import time

startTime = time.time()

f = open("testTxt_MD5_10000.txt", "r")
MD5.message = f.read()
MD5.fill_text()
result = MD5.process()
print("MD5:", format(result))

endTime = time.time()
f.close()

print("ND5用时：", endTime - startTime)
