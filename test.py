json_str={
   "1":["小花",99,100,98.5],
   "2":["小王",90,30.5,95],
   "3":["小明",67.5,49.6,88]
}
arrayM = []
for key in  json_str:
    tempArray = []
    tempArray.append(key)
    tempArray.append(json_str[key])
    arrayM.append(tempArray)
# print(arrayM)


# String = '123'
# print(String.replace('1','2'))

def is_back(s):
    return s[::-1]==(s if s.strip() else False)

print( is_back('heh'))
print('hello'[::-1])
import  time
print( time.localtime(time.time()))