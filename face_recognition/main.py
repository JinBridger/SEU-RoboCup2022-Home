from baidu_ai_face_detect import get_face_json
from baidu_ai_face_detect import get_bounding_box_num
from baidu_ai_face_detect import get_bounding_box_dict

from baidu_ai_face_load import get_face_tokens

from baidu_ai_face_compare import get_person_name

from plot_face_box import plot_face_box
from plot_face_box import plot_time_name

import os
import cv2


def main(persons_dir, photo_dir, output_dir):
    print("Preprocessing...")
    face_tokens = get_face_tokens(persons_dir)

    photonames = os.listdir(photo_dir)
    for photoname in photonames:
        print('Processing ' + photoname + '...')
        photo_filepath = photo_dir + '/' + photoname

        photo_num = "".join(list(filter(str.isdigit, photoname)))
        photo_num = str((int(photo_num) % 5) + 1)

        output_filepath = output_dir + '/Image' + photo_num + '.jpg'

        img = cv2.imread(photo_filepath)
        photo_face_json = get_face_json(photo_filepath)
        bounding_box_num = get_bounding_box_num(photo_face_json)
        bounding_box_dict = get_bounding_box_dict(photo_face_json)
        print('- Successfully get face dict...Now get their names...')

        face_cnt = 1
        for (face_key, face_value) in bounding_box_dict.items():
            print('-- Processing face ' + str(face_cnt) + '/' + str(bounding_box_num) + '...', end="")
            face_token = face_value['token']
            face_name = get_person_name(face_token, face_tokens)
            bounding_box_dict[face_key]['name'] = face_name
            face_cnt += 1
        for (face_key, face_value) in bounding_box_dict.items():
            img = plot_face_box(img,
                                face_value['location'],
                                face_value['name'],
                                face_value['gender'])
        img = plot_time_name(img)
        cv2.imwrite(output_filepath, img)



if __name__ == '__main__':
    persons = '/images/imageFace'
    photo = '/images/imageAfterOD'
    output = '/images/imageFinal'

    main(persons, photo, output)
