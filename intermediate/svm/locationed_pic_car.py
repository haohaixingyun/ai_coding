#here is on example for follow
#https://blog.csdn.net/weixin_41695564/article/details/79712393
#https://github.com/wzh191920/License-Plate-Recognition/blob/master/predict.py
#https://blog.csdn.net/weixin_41695564/article/details/79712393
import cv2
import numpy as  np
from numpy.linalg import norm
import sys
import os
import json

SZ = 20          #训练图片长宽
MAX_WIDTH = 1000 #原始图片最大宽度
Min_Area = 3000  #车牌区域允许最小面积
PROVINCE_START = 1000

#读取图片文件
img = cv2.imread("20190103123120.png")
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray_img',gray_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

rw ,cl = gray_img.shape[:2]
print(rw,cl)

if cl > MAX_WIDTH:
    change_rate = MAX_WIDTH / cl
    gray_img = cv2.resize(gray_img,(MAX_WIDTH,int(rw * change_rate)),interpolation=cv2.INTER_AREA)
    img = cv2.resize(img, (MAX_WIDTH, int(rw * change_rate)), interpolation=cv2.INTER_AREA)

gray_img = cv2.GaussianBlur(gray_img, (5,5), 0, 0, cv2.BORDER_DEFAULT)
kernel = np.ones((23, 23), np.uint8)
img_opening = cv2.morphologyEx(gray_img, cv2.MORPH_OPEN, kernel)
img_opening = cv2.addWeighted(gray_img, 1, img_opening, -1, 0)

# 找到图像边缘
ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img_edge = cv2.Canny(img_thresh, 100, 200)
#cv2.imshow('img_opening',img_edge)
## 使用开运算和闭运算让图像边缘成为一个整体
kernel = np.ones((18, 20), np.uint8)
img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)

img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)
cv2.imshow('img_edge2',img_edge2)

# # 查找图像边缘整体形成的矩形区域，可能有很多，车牌就在其中一个矩形区域中
image, contours, hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.waitKey(0)
temp_contours = []

for contour in contours:
        if cv2.contourArea( contour ) > Min_Area :
            print(cv2.contourArea( contour ))
            temp_contours.append(contour)
car_plate = []
print(len(temp_contours))
for temp_contour in temp_contours:
        rect_tupple = cv2.minAreaRect( temp_contour )
        rect_width, rect_height = rect_tupple[1]
        if rect_width < rect_height:
            rect_width, rect_height = rect_height, rect_width
        aspect_ratio = rect_width / rect_height
        # 车牌正常情况下宽高比在2 - 5.5之间
        print(aspect_ratio)
        if aspect_ratio > 2.4 and aspect_ratio < 5.5:
            car_plate.append( temp_contour )
            rect_vertices = cv2.boxPoints( rect_tupple )
            rect_vertices = np.int0( rect_vertices )

print(len(car_plate),'car_plate')
for car_plate in car_plate:
            row_min,col_min = np.min(car_plate[:,0,:],axis=0)
            print(row_min,col_min)
            row_max, col_max = np.max(car_plate[:, 0, :], axis=0)
            print(row_max, col_max)
            cv2.rectangle(img, (row_min,col_min), (row_max, col_max), (0,255,0), 2)
            card_img = img[col_min:col_max,row_min:row_max,:]
            cv2.imshow("img", img)
cv2.imwrite( "card_img.jpg",card_img )
cv2.imshow("card_img", card_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
