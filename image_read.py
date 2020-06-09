import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img_name = input('Please input your image path: ')
pic = mpimg.imread(img_name)

plt.imshow(pic)
plt.axis('off')
plt.show()