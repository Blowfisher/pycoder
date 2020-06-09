import copy
#常量拷贝
data = 1
data_2 = data

data_22 = 2
print('常量拷贝')
print(data, data_2)

#变量拷贝
data1 = [1,3,4]
data2 = data1
data2[1] = 2

print('变量拷贝')
print(data1,data2)




#浅拷贝
# 只会拷贝内容的父对象，顶层对象
data1 = [['data1', 'This is data1'], 1]
data2 = copy.copy(data1)
print(id(data1),id(data2))
data2[0][0] = 'data2'
data2[1] = 2
print('浅拷贝')
print('data1 :', data1, 'data2 :', data2)

#深拷贝
data1 = [['data1', 'This is data1'], 1]
data2 = copy.deepcopy(data1)


data2[0][0] = 'data2'
data2[1] = 2
print('深拷贝')
print('data1 :', data1, 'data2 :', data2)

a = 1
def var_test(*args,**xargs):
    for i in args:
        print(i)
    for k in xargs:
        print('key is {0},value is {1}'.format(k,xargs[k]))

var_test(1,2,3,name='bambo',age=18)