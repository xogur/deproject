import requests
import re, json
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json,re
import base64


def trend():

    # 특정 요소(미니멀, 남자)스냅 페이지 들어기기
    cookies = {
        '_gf': 'A',
        'tr[vid]': '67dcc9ed80d478.78189875',
        'tr[vd]': '1742522861',
        '_ga': 'GA1.1.2014950775.1742522862',
        '_gcl_au': '1.1.1173424347.1742522862',
        '_kmpid': 'km|musinsa.com|1742522862391|8bed8223-fe1b-4702-a9ff-df8d0ca43824',
        '_fbp': 'fb.1.1742522862889.61970195871643448',
        '_fwb': '1557zuEgyrlkclzlKZTqlUc.1742522862899',
        '_pin_unauth': 'dWlkPU9UWTRaVFZtWXpJdE5XVmlPQzAwWW1WakxXSXpNVFl0TlRGalkyVXhOekV6T0dJNQ',
        '_hjSessionUser_1491926': 'eyJpZCI6IjM4YmQ2OThkLTMyY2MtNTIxNi1hOWNmLTFmN2MzN2E4ZTI0NiIsImNyZWF0ZWQiOjE3NDI1MjI4NjI5MTcsImV4aXN0aW5nIjp0cnVlfQ==',
        '_tt_enable_cookie': '1',
        '_ttp': '01JPV7AKAA8M0D5JH5FH4N16B3_.tt.1',
        'cart_no': 'x4cYG0jKxoPy11Hca%2F4hvNL%2FJlQrtTNAe1nKIT3RZlY%3D',
        '_hjSession_1491926': 'eyJpZCI6IjRlODg4NDg4LTA5MjEtNGZiZS04NmRiLWRmYWNlMTkyNDVmNSIsImMiOjE3NDM1OTUwNzA3MzEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        'ab.storage.deviceId.1773491f-ef03-4901-baf8-dbf84e1de25b': '%7B%22g%22%3A%229fa9d012-1d4c-a302-ef6e-7adb457cf56e%22%2C%22c%22%3A1742522895703%2C%22l%22%3A1743596015889%7D',
        'snap_interest': 'd86886a5-26eb-4d80-9393-d85a80de4666',
        'ab.storage.sessionId.1773491f-ef03-4901-baf8-dbf84e1de25b': '%7B%22g%22%3A%22da9b78ff-b445-ac2c-37b1-9eb2b76e7e69%22%2C%22e%22%3A1743597831729%2C%22c%22%3A1743596015888%2C%22l%22%3A1743596031729%7D',
        'tr[vt]': '1743596273',
        'tr[vc]': '2',
        'tr[pv]': '2',
        'cto_bundle': 'NR4Rp19DWXB3OTN4bXRnSmJmOW5GNmozRGRTSnN3dkxhN0dNZ1E0JTJGYmlLQTVLOE43UHY1MGhmc1FDUG9kc3RFa3olMkJBN2FlVHVScTJtb0hocDF6SyUyRnRDZnM0c1ZTc0d3OHlLa1RNNWpsZmdaNklKZGVaR21RYktYYWVIOFNOaGs0RDFUSnJ4V2lrbG1JcHVJN0ZZelB6YzNFQ0ElM0QlM0Q',
        'AMP_74a056ea4a': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyMjNkZmIxNC1hNGVhLTRlNmQtYjY3ZS02YzhjODAzYWFlMGElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQzNTk1ODE1MjMxJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlN0Q=',
        '_ga_8PEGV51YTJ': 'GS1.1.1743595069.4.1.1743596397.48.0.0',
        'AMP_TLDTEST': 'MQ==',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer null',
        'origin': 'https://www.musinsa.com',
        'priority': 'u=1, i',
        'referer': 'https://www.musinsa.com/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        # 'cookie': '_gf=A; tr[vid]=67dcc9ed80d478.78189875; tr[vd]=1742522861; _ga=GA1.1.2014950775.1742522862; _gcl_au=1.1.1173424347.1742522862; _kmpid=km|musinsa.com|1742522862391|8bed8223-fe1b-4702-a9ff-df8d0ca43824; _fbp=fb.1.1742522862889.61970195871643448; _fwb=1557zuEgyrlkclzlKZTqlUc.1742522862899; _pin_unauth=dWlkPU9UWTRaVFZtWXpJdE5XVmlPQzAwWW1WakxXSXpNVFl0TlRGalkyVXhOekV6T0dJNQ; _hjSessionUser_1491926=eyJpZCI6IjM4YmQ2OThkLTMyY2MtNTIxNi1hOWNmLTFmN2MzN2E4ZTI0NiIsImNyZWF0ZWQiOjE3NDI1MjI4NjI5MTcsImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ttp=01JPV7AKAA8M0D5JH5FH4N16B3_.tt.1; cart_no=x4cYG0jKxoPy11Hca%2F4hvNL%2FJlQrtTNAe1nKIT3RZlY%3D; _hjSession_1491926=eyJpZCI6IjRlODg4NDg4LTA5MjEtNGZiZS04NmRiLWRmYWNlMTkyNDVmNSIsImMiOjE3NDM1OTUwNzA3MzEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; ab.storage.deviceId.1773491f-ef03-4901-baf8-dbf84e1de25b=%7B%22g%22%3A%229fa9d012-1d4c-a302-ef6e-7adb457cf56e%22%2C%22c%22%3A1742522895703%2C%22l%22%3A1743596015889%7D; snap_interest=d86886a5-26eb-4d80-9393-d85a80de4666; ab.storage.sessionId.1773491f-ef03-4901-baf8-dbf84e1de25b=%7B%22g%22%3A%22da9b78ff-b445-ac2c-37b1-9eb2b76e7e69%22%2C%22e%22%3A1743597831729%2C%22c%22%3A1743596015888%2C%22l%22%3A1743596031729%7D; tr[vt]=1743596273; tr[vc]=2; tr[pv]=2; cto_bundle=NR4Rp19DWXB3OTN4bXRnSmJmOW5GNmozRGRTSnN3dkxhN0dNZ1E0JTJGYmlLQTVLOE43UHY1MGhmc1FDUG9kc3RFa3olMkJBN2FlVHVScTJtb0hocDF6SyUyRnRDZnM0c1ZTc0d3OHlLa1RNNWpsZmdaNklKZGVaR21RYktYYWVIOFNOaGs0RDFUSnJ4V2lrbG1JcHVJN0ZZelB6YzNFQ0ElM0QlM0Q; AMP_74a056ea4a=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyMjNkZmIxNC1hNGVhLTRlNmQtYjY3ZS02YzhjODAzYWFlMGElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQzNTk1ODE1MjMxJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlN0Q=; _ga_8PEGV51YTJ=GS1.1.1743595069.4.1.1743596397.48.0.0; AMP_TLDTEST=MQ==',
    }
    data = {}
    id_list = []

    for i in range(1, 3) :
        params = {
            'formatTypes': 'POST,SHORTS',
            'bodyHeightRange': '',
            'bodyWeightRange': '',
            'brands': '',
            'contentTypes': '',
            'genders': 'MEN',
            'goodsCategories': '',
            'seasonLabels': '4',
            'sort': 'POPULAR',
            'styleLabels': '5',
            'tpoLabels': '',
            'page': i,
            'size': '24',
            'excludedSnapIds': id_list,
        }
        # 스냅
        res = requests.get(
            'https://content.musinsa.com/api2/content/snap/ui/v2/modules/discovery/sections',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        for idd in json.loads(res.text)['data']['list'][0]['contents']:
            id_list.append(idd['id'])
        for element in (json.loads(res.text)['data']['list'][0]['contents']) :
            
            params = {
                'formatTypes': 'POST,SHORTS',
                'page': '1',
                'size': '10',
            }

            # 스냅샷 상세보기
            response = requests.get(
                f'https://content.musinsa.com/api2/content/snap/v1/snaps/{element['id']}/recommendations',
                params=params,
                cookies=cookies,
                headers=headers,
            )

            if response.status_code != 200:
                continue

            for product in (json.loads(response.text)['data']['list'][0]['goods']) :
        
                product_res = requests.get(f'https://www.musinsa.com/products/{product['goodsNo']}', cookies=cookies, headers=headers)
                soup = BeautifulSoup(product_res.text, "html.parser")
                html = soup.select_one("script#category-data")
                try:
                    pattern = r'window\.__MSS__\.product\.state\s*=\s*(\{.*?\})?;'
                    match = re.search(pattern, html.text, re.DOTALL)
                    if match:
                        result = match.group(1)
                        product_name = json.loads(result)['goodsNm']
                        image = "https://image.msscdn.net/thumbnails" + json.loads(result)['thumbnailImageUrl']
                    else:
                        print("패턴 불일치")
                except Exception as e:
                    print(f"해당 상품은 존재하지 않습니다: {e}")
                    continue
                    
                if product_name in data:
                    data[product_name]["count"] += 1
                else:
                
                
                    params = {
                        'goodsSaleType': 'SALE',
                        'optKindCd': 'CLOTHES',
                    }
                    
                    color_res = requests.get(
                        f'https://goods-detail.musinsa.com/api2/goods/{product['goodsNo']}/v2/options',
                        params=params,
                        cookies=cookies,
                        headers=headers,
                    )
                    if json.loads(color_res.text)['data']['basic'][0]['name'] == '컬러' :
                        color = json.loads(color_res.text)['data']['basic'][0]['optionValues'][0]['name']
                    else :
                        color = ""
                        
                    data[product_name] = {
                        "color": color,
                        "image": image,
                        "count": 1
                    }
    df = pd.DataFrame.from_dict(data, orient='index').reset_index()
    df = df.rename(columns={"index": "product_name"})
    return df