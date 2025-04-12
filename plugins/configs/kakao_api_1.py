import pendulum
from dateutil.relativedelta import relativedelta
import os
import json
import requests
from airflow.models import Variable

REDIRECT_URL = 'https://example.com/oauth'

def _refresh_token_to_variable():
    client_id = Variable.get("kakao_client_secret")
    tokens = eval(Variable.get("kakao_tokens"))
    refresh_token = tokens.get('refresh_token')
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": f"{client_id}",
        "refresh_token": f"{refresh_token}"
    }
    response = requests.post(url, data=data)
    rslt = response.json()
    new_access_token = rslt.get('access_token')
    new_refresh_token = rslt.get('refresh_token')         # Refresh 토큰 만료기간이 30일 미만이면 refresh_token 값이 포함되어 리턴됨.
    if new_access_token:
        tokens['access_token'] = new_access_token
    if new_refresh_token:
        tokens['refresh_token'] = new_refresh_token

    now = pendulum.now('Asia/Seoul').strftime('%Y-%m-%d %H:%M:%S')
    tokens['updated'] = now
    os.system(f'airflow variables set kakao_tokens "{tokens}"')
    print('variable 업데이트 완료(key: kakao_tokens)')


# https://image.msscdn.net/thumbnails/images/goods_img/20240131/3836412/3836412_17084990134555_big.jpg?w=1200
def send_kakao_msg(product_name: str, old_price: int, price: int, product_link: str):
    '''
    content:{'tltle1':'content1', 'title2':'content2'...}
    '''

    try_cnt = 0
    while True:
        # Access Token 가져오기
        tokens = json.loads(Variable.get("kakao_tokens"))
        access_token = tokens.get('access_token')

        # 커머스 메시지 템플릿 구성
        template_object = {
            "object_type": "commerce",
            "content": {
                "title": product_name,
                "image_url": "https://image.msscdn.net/thumbnails/images/goods_img/20240131/3836412/3836412_17084990134555_big.jpg?w=1200",
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": product_link,
                    "mobile_web_url": product_link
                }
            },
            "commerce": {
                "regular_price": old_price,
                "discount_price": price
            },
            "buttons": [
                {
                    "title": "상품 보러가기",
                    "link": {
                        "web_url": product_link,
                        "mobile_web_url": product_link
                    }
                }
            ]
        }

        send_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {
            "Authorization": f'Bearer {access_token}'
        }
        data = {'template_object': json.dumps(template_object)}
        response = requests.post(send_url, headers=headers, data=data)
        print(f'try횟수: {try_cnt}, reponse 상태:{response.status_code}')
        try_cnt += 1

        if response.status_code == 200:         # 200: 정상
            return response.status_code
        elif response.status_code == 400:       # 400: Bad Request (잘못 요청시), 무조건 break 하도록 return
            return response.status_code
        elif response.status_code == 401 and try_cnt <= 2:      # 401: Unauthorized (토큰 만료 등)
            _refresh_token_to_variable()
        elif response.status_code != 200 and try_cnt >= 3:      # 400, 401 에러가 아닐 경우 3회 시도때 종료
            return response.status_code