import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0.0,5.0,0.001)
y = 220*np.sin(100*np.pi*x)

plt.plot(x,y,color="black")
plt.xlabel('time(s)')
plt.ylabel('volts(V)')
plt.show()
