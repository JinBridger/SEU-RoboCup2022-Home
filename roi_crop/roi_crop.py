import cv2
import numpy as np
from imutils.perspective import four_point_transform
from filter import add_curve
import os


def my_approx(con):  # con为预先得到的最大轮廓
    num = 0.001
    # 初始化时不需要太小，因为四边形所需的值并不很小
    ep = num * cv2.arcLength(con, True)
    con = cv2.approxPolyDP(con, ep, True)
    while True:
        if len(con) <= 4:  # 防止程序崩溃设置的<=4
            break
        else:
            num = num * 1.5
            ep = num * cv2.arcLength(con, True)
            con = cv2.approxPolyDP(con, ep, True)
            continue
    return con


def roi_crop(input_img):
    ori_img = input_img

    gray_img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    diff_img = cv2.cvtColor(ori_img - gray_img, cv2.COLOR_BGR2GRAY)
    retval, dst_img = cv2.threshold(diff_img, 1, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(dst_img, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    area = []
    for k in range(len(contours)):
        area.append(cv2.contourArea(contours[k]))
    max_idx = np.argmax(np.array(area))

    rect = my_approx(contours[max_idx])
    crop_img = four_point_transform(ori_img, rect.reshape(4, 2))

    return crop_img


if __name__ == '__main__':
    # img = cv2.imread(r"C:\Users\26354\Documents\RoboCup_home\roi_crop\image\input\image1.png")
    # roi_crop(img)
    # cv2.waitKey(0)

    input_dir = "/home/mrziyi/RoboCup/Final/images/imageTaken"
    output_dir = "/home/mrziyi/RoboCup/Final/images/imageAfterRoI"
    curve_path = "/home/mrziyi/RoboCup/Final/catkin_ws/roi_crop/image/curve/curve_adj.acv"

    filenames = os.listdir(input_dir)
    for filename in filenames:
        if filename.endswith('.ini'):
            continue
        input_img = cv2.imread(input_dir + '/' + filename)
        output_img = roi_crop(input_img)
        if filename.endswith('2.jpg') or filename.endswith('3.jpg') or filename.endswith('7.jpg') or filename.endswith('8.jpg'):
            output_img = add_curve(output_img, curve_path)
        cv2.imwrite(output_dir + '/' + filename, output_img)
