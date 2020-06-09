import csv
import matplotlib.pyplot as plt

word = []
num = []
sum = 0

file_name = input('Please input your file path: ')

with open(file_name,'r') as file:
    items = csv.reader(file,delimiter=',')
    print(items)
    for item in items:
        print(item)
        word.append(item[0])
        re_num = (int(item[1]))
        num.append(int(re_num))
        sum += int(re_num)


x = []
y = []

for i in range(10):
    x.append(word[i])
    y.append(num[i]/sum*100)


plt.bar(x,y)
plt.xlabel('word')
plt.ylabel('probability(%)')
plt.show()