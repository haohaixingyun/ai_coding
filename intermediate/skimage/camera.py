from  skimage import  data , filters ,io
import  matplotlib.pyplot as plt
imag1e = data.camera()
image =io.imread('D:\\sthself\\尼泊尔\\IMG_2167.JPG',as_grey=True)
dst = filters.threshold_adaptive(image,57)
print(dst)
plt.figure("thresh",figsize=(8,8))

plt.subplot(121)
plt.title('original image')
plt.imshow(image,plt.cm.gray)
plt.subplot(122)
plt.title('binary image')
plt.imshow(dst,plt.cm.gray)
plt.show()