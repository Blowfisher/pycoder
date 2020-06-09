import matplotlib.pyplot as plt

x = [1,3,5,7,9,11]
y = [4,1,5,7,10,5]

plt.scatter(x,y,label = "scatter",s=15,marker="*")

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title("Bambo 散点图")
plt.legend()
plt.show()