import random
import datetime

import cv2
from baidu_ai_face_detect import get_bounding_box_dict, get_face_json


def plot_one_box(x, img, color=(0, 255, 255), label='person', line_thickness=3):
    """

    :param x: 坐标点
    :param img: 图片
    :param color: 三原色值
    :param label: 标注名
    :param line_thickness:  线框厚度
    :return:
    """
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    return img


def plot_face_box(img, bounding_box, name, gender):
    if name == 'Others':
        return img
    label = name + '_' + gender
    return plot_one_box(bounding_box, img, (255, 0, 0), label)


def plot_time_name(img):
    time_str = str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    name_str = 'Team: Unknown'
    leader_str = 'Leader: Unknown'
    img = cv2.putText(img, name_str, (10, 20), 0, 0.5,
                      (255, 0, 0), 1, cv2.LINE_AA)
    img = cv2.putText(img, leader_str, (10, 40), 0, 0.5,
                      (255, 0, 0), 1, cv2.LINE_AA)
    img = cv2.putText(img, time_str, (10, 60), 0, 0.5,
                        (255, 0, 0), 1, cv2.LINE_AA)
    return img


if __name__ == '__main__':
    img = cv2.imread('jpg_path')
    img = plot_time_name(img)
    cv2.imshow("img", img)
    cv2.waitKey(0)
