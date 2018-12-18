from skimage import  io
import matplotlib.pyplot as  plt

photo = io.imread("../aftImage/20081203235732890ch5IMG.JPG")
io.imshow(photo)
plt.show()