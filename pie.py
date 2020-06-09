import matplotlib.pyplot as plt

Score = [95,89,65,90,77]
Subject = ['Math','Chinese','English','Synthetical','Bambo']
cols = ['c','m','r','b','g']

plt.pie(
    Score,
    labels = Subject,
    colors = cols,
    startangle = 90,
    shadow = False,
    explode = (0,0.05,0,0,0),
    autopct = '%1.1f%%')

plt.title('Bambo 饼图')
plt.show()