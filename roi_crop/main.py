import os.path
import sys
import cv2
from roi_crop import roi_crop
from filter import add_curve


if __name__ == '__main__':
    output_dir = "/images/imageAfterRoI"
    curve_path = "/image/curve/curve_adj.acv"

    img_path = sys.argv[1]
    img_name = os.path.basename(img_path)

    input_img = cv2.imread(img_path)
    output_img = roi_crop(input_img)
    if img_path.endswith('2.png') or img_path.endswith('3.png'):
        output_img = add_curve(output_img, curve_path)
    
    cv2.imshow("img", output_img)
    cv2.waitKey(0)
    
    cv2.imwrite(output_dir + '/' + img_name, output_img)
