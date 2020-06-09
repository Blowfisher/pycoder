import matplotlib.pyplot as plt

x1 = [1,3,5,7,9,11]
y1 = [14,1,5,7,10,5]

x2 = [2,4,6,8,10,11]
y2 = [1,3,9,2,11,2]

plt.bar(x1,y1,label = 'bar1')
plt.bar(x2,y2,label = 'bar2')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')

plt.title('Bambo bar')
plt.legend()
plt.show()

