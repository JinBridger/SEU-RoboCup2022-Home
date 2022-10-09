import requests
import base64
import os
import time


def jpg_to_base64(jpg_filepath):
    # resize jpg to 2M if oversize

    # convert to base64
    img = open(jpg_filepath, 'rb')
    base64_code = base64.b64encode(img.read())
    return str(base64_code, 'utf-8')


def get_one_face_token(jpg_filepath):
    jpg_base64 = jpg_to_base64(jpg_filepath)

    face_params = '{"image":"' + jpg_base64 + '",' + \
                  '"image_type":"BASE64",' + \
                  '"max_face_num": 1,' + \
                  '"face_field":"faceshape,gender"}'

    request_url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
    access_token = ''
    request_url = request_url + '?access_token=' + access_token
    headers = {'content-type': 'application/json'}

    response = requests.post(request_url, data=face_params, headers=headers)

    while response.json()['error_code'] != 0:
        print('- Process failed with error code ' + str(response.json()['error_code']) + ', retrying...')
        response = requests.post(request_url, data=face_params, headers=headers)

    return response.json()['result']['face_list'][0]['face_token']


def get_face_tokens(jpg_filedir):
    jpg_filenames = os.listdir(jpg_filedir)
    token_dict = {}

    face_cnt = 1
    for jpg_filename in jpg_filenames:
        time.sleep(0.7)
        person_name = os.path.splitext(jpg_filename)[0]
        token_dict[person_name] = get_one_face_token(jpg_filedir + '/' + jpg_filename)
        print('- Preprocess succeed ' + str(face_cnt) + '/' + str(len(jpg_filenames)))
        face_cnt += 1

    return token_dict


if __name__ == '__main__':
    print(get_face_tokens(''))