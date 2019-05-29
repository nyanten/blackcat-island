# coding:utf-8

import os
import cv2

dir_path = os.getcwd()
yuina_path = "images/Yuina/"
outputs = os.path.join(dir_path, "outputs/")
# haar-like
cv_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"

def main():
    imgs_path = os.path.join(dir_path, yuina_path)

    img = cv2.imread(yuina_path+"000002.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 特徴量取得
    cascade = cv2.CascadeClassifier(cv_path)

    face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

    if len(face) > 0:
        for rect in face:
            cv2.imwrite(outputs + "1.jpg", img[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])



if __name__ == '__main__':
    main()
