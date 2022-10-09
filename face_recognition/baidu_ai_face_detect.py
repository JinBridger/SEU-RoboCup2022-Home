import requests
import base64


def jpg_to_base64(jpg_filepath):
    # resize jpg to 2M if oversize

    # convert to base64
    img = open(jpg_filepath, 'rb')
    base64_code = base64.b64encode(img.read())
    return str(base64_code, 'utf-8')


def get_face_json(jpg_filepath):
    jpg_base64 = jpg_to_base64(jpg_filepath)

    face_params = '{"image":"' + jpg_base64 + '",' + \
                  '"image_type":"BASE64",' + \
                  '"max_face_num": 5,' + \
                  '"face_field":"faceshape,gender"}'

    request_url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
    access_token = ''
    request_url = request_url + '?access_token=' + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=face_params, headers=headers)

    return response.json()


def get_bounding_box_num(face_json):
    return face_json['result']['face_num']


def get_bounding_box_dict(face_json):
    face_list = face_json['result']['face_list']
    ret_dict = {}
    face_num = 1

    for face_dict in face_list:
        ret_dict[str(face_num)] = {}
        for (item_key, item_value) in face_dict.items():
            if item_key == 'location':
                bounding_box_list = []

                face_x1 = round(item_value['left'])
                face_y1 = round(item_value['top'])
                face_x2 = round(face_x1 + item_value['width'])
                face_y2 = round(face_y1 + item_value['height'])

                bounding_box_list.append(face_x1)
                bounding_box_list.append(face_y1)
                bounding_box_list.append(face_x2)
                bounding_box_list.append(face_y2)

                ret_dict[str(face_num)]['location'] = bounding_box_list
            if item_key == 'gender':
                gender = item_value['type']
                ret_dict[str(face_num)]['gender'] = gender
            if item_key == 'face_token':
                ret_dict[str(face_num)]['token'] = item_value

        face_num += 1

    return ret_dict


if __name__ == '__main__':
    img_path = "jpg_path"
    print(get_bounding_box_dict(get_face_json(img_path)))