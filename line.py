import matplotlib.pyplot as plt
x1 = [1,3,4]
y1 = [2,4,1]
x2 = [1,3,4]
y2 = [4,1,5]
x3 = [1,2,3]
y3 = [1,4,9 ]

plt.plot(x1,y1,label='Line1',color = "red")
plt.plot(x2,y2,label = 'Line2',color = '#191919')
plt.plot(x3,y3,label = 'Line3',color = 'b')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Bambo Graph')
plt.legend()
plt.show()