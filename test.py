import random
lowString = 'abcdefghijklmnopqrstuvwxyz'
upString = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'
allArray = lowString+upString+num
times = int(input('请输入次数'))
def setUpRandomNum(k,arrayStr = []):
    x = random.sample(allArray,8)
    a = len(list(set(x).intersection(set(lowString)))) > 0
    b = len(list(set(x).intersection(set(upString)))) > 0
    c = len(list(set(x).intersection(set(num))))>0
    d = not (k in arrayStr)
    if a and b and c and d:
        k = k-1
        arrayStr.append(''.join(x))
    if k == 0:
        return arrayStr
    else:
        return setUpRandomNum(k,arrayStr)

print(setUpRandomNum(times))

