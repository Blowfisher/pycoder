import math,random
n = 0
m = 100000
#边长为2的正方形 求起内切圆
#math.pow 与pow 区别在于math.pow精度为1 pow精度位数为0
for i in range(m):
#random.random() 默认生成0 - 1 之间的数
    x = random.random()*2
    y = random.random()*2
    if  math.pow(x-1,2) + math.pow(y-1,2) <=1:
        n += 1
pi_prob = n/m*4
print('The pi is {0}'.format(pi_prob))