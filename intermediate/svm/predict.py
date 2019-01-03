from sklearn.externals import joblib
from skimage import io

#model = joblib.load('../txt/svm_job_modle.m')  # 模型的重载
#class_predict = model.predict(featuretest)

for x in range(1):

    img = io.imread("character0.jpg",as_grey=True)
    io.imshow(img)
    print(img.shape)
    img.reshape(92,47)
    io.show()




