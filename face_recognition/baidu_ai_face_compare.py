import requests
import time


def compare_two_faces(face_token_1, face_token_2):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"

    params = '[{"image": "' + face_token_1 + \
             '", "image_type": "FACE_TOKEN", "face_type": "LIVE", "quality_control": "NONE"},' \
             '{"image": "' + face_token_2 + \
             '", "image_type": "FACE_TOKEN", "face_type": "LIVE", "quality_control": "NONE"}]'

    access_token = ''
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)

    while response.json()['error_code'] != 0:
        print('--- Failed with code ' + str(response.json()['error_code']) + ', retrying...')
        response = requests.post(request_url, data=params, headers=headers)

    return response.json()['result']['score']


def get_person_name(face_token, face_tokens):
    similarity = {}

    cur_face = 1
    for (item_key, item_value) in face_tokens.items():
        time.sleep(0.7)
        similarity[item_key] = compare_two_faces(face_token, item_value)
        print(str(cur_face), end="")
        cur_face += 1
    print('...OK!')

    similarity = sorted(similarity.items(), key=lambda d: d[1], reverse=True)

    if similarity[0][1] < 80:
        return 'Others'
    else:
        return similarity[0][0]


if __name__ == '__main__':
    pass