num= 22
den=11
des=2
done = False
que = num//den
for cnt in range(0,des+1):
    #print(que)
    num = num - (den * que);
    if num == 0:
        print('0',end='')
        done = True
        break
    num = num*10
    que = num//den
if not done:
    print(que)
