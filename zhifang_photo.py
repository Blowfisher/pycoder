import matplotlib.pyplot as plt

data = [5,22,10,44,55,99,87,86,45,22,6,33,87,98,15,25,77,89,31,71,83,82,52]
scalr = [0,10,20,30,40,50,60,70,80,90,100]
plt.hist(data,scalr,histtype='barstacked',rwidth=0.5)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Bambo hist')
plt.legend()
plt.show()