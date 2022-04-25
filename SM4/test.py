T = int(input())
cnt = 0
flag = False
for i in range(T):
    str = input().split()
    if "SkaditheCorruptingHeart" in str:
        flag = True
        break

cnt = (T + 5) // 6

if flag:
    print ("ILOVESENRUA{:d}".format(3000 - cnt  * 648))
else:
    print ("OCEANCAT")