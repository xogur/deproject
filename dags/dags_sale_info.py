from airflow import DAG
import pendulum
import datetime
from airflow.operators.python import PythonOperator
import random
from airflow.models import Variable

with DAG(
    dag_id="dags_python_operator",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    def crawling_sale():
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        import pyperclip
        import time
        import requests
        import json
        import pandas as pd
        import sys
        import os

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")  # (optional but often helps)
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')
        driver = webdriver.Chrome(options=options)

        time.sleep(1)
        driver.get("https://www.musinsa.com/mypage")
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#__next > div > div.SignInUp__Container-sc-1wbn3h6-0.hjEKVr > div > a > span").click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "#commonLayoutContents > section > div.login-v2-member > div > div > a.login-v2-button__item.login-v2-button__item--kakao.gtm-click-button").click()
        time.sleep(1)

        id = driver.find_element(By.CSS_SELECTOR, '#loginId--1')
        id.click()
        id.send_keys(Variable.get("your_id"))
        # pyperclip.copy(your_id)
        # id.send_keys(Keys.CONTROL, 'v')
        #driver.execute_script(f"document.querySelector('#loginId--1').value = '{your_id}';")
        driver.save_screenshot("screenshot1.png")
        time.sleep(1)

        pw = driver.find_element(By.CSS_SELECTOR, '#password--2')
        pw.click()
        pw.send_keys(Variable.get("your_pw"))
        # pyperclip.copy(your_pw)
        # pw.send_keys(Keys.CONTROL, 'v')
        #driver.execute_script(f"document.querySelector('#password--2').value = '{your_pw}';")
        time.sleep(1)
        driver.save_screenshot("screenshot2.png")

        driver.find_element(By.CSS_SELECTOR, "#mainContent > div > div > form > div.confirm_btn > button.btn_g.highlight.submit").click()
        time.sleep(1)
        driver.save_screenshot("screenshot3.png")
        cookies = driver.get_cookies()

        session = requests.Session()

        cursor = ''
        product_list = []

        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        while True:
            headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
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
            # 'cookie': '_gf=A; tr[vid]=67dcc9ed80d478.78189875; tr[vd]=1742522861; _ga=GA1.1.2014950775.1742522862; _gcl_au=1.1.1173424347.1742522862; _kmpid=km|musinsa.com|1742522862391|8bed8223-fe1b-4702-a9ff-df8d0ca43824; _fbp=fb.1.1742522862889.61970195871643448; _fwb=1557zuEgyrlkclzlKZTqlUc.1742522862899; _pin_unauth=dWlkPU9UWTRaVFZtWXpJdE5XVmlPQzAwWW1WakxXSXpNVFl0TlRGalkyVXhOekV6T0dJNQ; _hjSessionUser_1491926=eyJpZCI6IjM4YmQ2OThkLTMyY2MtNTIxNi1hOWNmLTFmN2MzN2E4ZTI0NiIsImNyZWF0ZWQiOjE3NDI1MjI4NjI5MTcsImV4aXN0aW5nIjp0cnVlfQ==; _tt_enable_cookie=1; _ttp=01JPV7AKAA8M0D5JH5FH4N16B3_.tt.1; AMP_74a056ea4a=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyMjNkZmIxNC1hNGVhLTRlNmQtYjY3ZS02YzhjODAzYWFlMGElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQzNTk1ODE1MjMxJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlN0Q=; cart_no=x4cYG0jKxoPy11Hca%2F4hvNL%2FJlQrtTNAe1nKIT3RZlY%3D; viewKind=3GridView; _hjSession_1491926=eyJpZCI6IjNlMzJmODI3LWJmZTAtNDNhYS04YjVmLTQ3MDNiMjIzNGY2YiIsImMiOjE3NDM5NDA1ODk1NjAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ds_sessions=y; ab.storage.deviceId.1773491f-ef03-4901-baf8-dbf84e1de25b=%7B%22g%22%3A%229fa9d012-1d4c-a302-ef6e-7adb457cf56e%22%2C%22c%22%3A1742522895703%2C%22l%22%3A1743940662298%7D; ab.storage.userId.1773491f-ef03-4901-baf8-dbf84e1de25b=%7B%22g%22%3A%2200596e2163db6a13ed779dc23dec610e%22%2C%22c%22%3A1743940662298%2C%22l%22%3A1743940662299%7D; easyPayInfoData=%7B%22hashId%22%3A%2200596e2163db6a13ed779dc23dec610e%22%2C%22data%22%3A%7B%22payKind%22%3A%22NAVERPAY%22%2C%22existPickupOrder%22%3Afalse%2C%22existOnlineOrder%22%3Atrue%2C%22pickupShopNo%22%3A0%7D%7D; ab.storage.sessionId.1773491f-ef03-4901-baf8-dbf84e1de25b=%7B%22g%22%3A%22362f6748-b690-84c0-0460-63091536bf4f%22%2C%22e%22%3A1743942826568%2C%22c%22%3A1743940662298%2C%22l%22%3A1743941026568%7D; tr[vt]=1743941832; tr[vc]=5; app_rtk=4492904f10182dd0e780a337ca83ee62223081ea; mss_last_login=20250406; mss_mac=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwMDU5NmUyMTYzZGI2YTEzZWQ3NzlkYzIzZGVjNjEwZSIsImhhc2hlZEVtYWlsIjoiMmFjMDViMGVmNmE0MmM5OWE1MzVjYTE1N2MwZDVhYjc2MjUwOWViNzAxZTU2ZDFjMjM5M2VhODI5MDhkYmQ2ZiIsImdlbmRlciI6Ik0iLCJvcmRlckNvdW50IjoiNzYiLCJzZWxmQ2VydGlmeSI6dHJ1ZSwiaGFzaElkIjoiMDA1OTZlMjE2M2RiNmExM2VkNzc5ZGMyM2RlYzYxMGUiLCJtZW1iZXJHcm91cExpc3QiOlsiU05BUF9VU0VSIl0sImJpcnRoWWVhciI6IjIwMDAiLCJvcmRlckFtb3VudFJhbmdlIjoiNjAw66eM7JuQ64yAIiwibmlja25hbWUiOiLqtp3tg7HtmJUiLCJhZ2VCYW5kIjoiMjUiLCJncm91cExldmVsIjoiNiIsImV4cCI6MTc3NTQ3NjY1OCwiaWF0IjoxNzQzOTQwNjU4LCJyZWdpc3RlckRhdGUiOiIyMDE5LTAyLTExIiwidXNlckJ1Y2tldCI6Ijc5In0.neHzEEq9z0gfQaWAiZG1VMECv7R0ZLlV7KX6Uo4S40c; app_atk=ObIaW2MbM9Wh6tKU1mdA7ry0IK5GQcu0rksuG53SkafbOwmPHGnmwtUrAKSfUT8KDgVy7fAVc2bMwqVjrM%2BbOLNKmL0DpOrRkQnaVIKMY2EsG3FL1P1LPGw1Y5hlbsolGL763D8dd4MM8iXwoa8ht9OFx3uavNkAaG2SqezIPLPszrEnletYnzGUewwal9dllaYNTzL99cYMhpZ9U7hiP2fTANUVBTiW5QAX8ApBSrakS2QVB62oR832bz8RyU5mAFdwO44m5WFptTcUEacyNR4p%2FHLj029Z%2B1iHm6QGSjwUQirO4NWhicDpZZxLOeMXStcn7uq33smxJNUpjDUP5YfBB7%2BPz92qJwIWdfQI6Aw1ndlCdw9FgqD3hwdjVAq95rI9jV1Kddo76JArYyLrEomf7TOc3wWXXtR%2Bg9PFe8pvqPgDvTpFyFlJjqMMQLTFT9xxDmwp%2FI5Za8dNvp3m2G9k4pRlL%2B499V9%2BXVmXH3D%2FcPLO3K%2BP2GLrJRrngcnTAfdOERk9J%2FHsYfKnmotuBNcLqNbV6l8ulNnmdY0FfO0nLcExeifxGdIHJjPW5tUMSrmSReAXdKDf8g4AMDkAT2YG081Ti0u45ixpGvOM1DwRuACakXE1EoYkZ0rF7r8%2BOiAezjQcy1MK0YdAKd2ozJ019V%2BcAvN16Ahem1iugBsq0qttkoGSpNRsFmeFOQTNAeSSGMmC52wRxfdVqYaPgXqCxmOK%2BC%2BhmEd4aPkNiUvHMpr%2B3Rw9QNkAV2mrJG7o; cto_bundle=GA4u3l9DWXB3OTN4bXRnSmJmOW5GNmozRGRUaiUyRlpmYmsxMVFEQU9YeDEzS1V2JTJGWkZocjNJNnlweFUlMkIlMkJGNmRONVE2U0FkWXBObERlenZCNFlTTlElMkJJcjhZRDVXRFdxNTlZTE1UR3RxRjE3V2t1ZUdERVowcnZCJTJCaXZUV2poNk1XTlYlMkZsUDQyJTJCUnBCQXY3VDQ2M1VzJTJGQnVkclpIZnRveVZ0UUtoQ1d4UWtJa3VBdXR3TDJqMk9KbU5nSFJnYUJQVjV6dUN3T0RWWDdXZDVua0RLSUNBbzl0ZkhRJTNEJTNE; tr[pv]=5; _ga_8PEGV51YTJ=GS1.1.1743940589.8.1.1743941843.48.0.0',
            }
            
            params = {
                'isSale': 'false',
                'isNotSoldOut': 'true',
                'sort': 'LIKE_MEMBER_ID_DESC',
                'size': '30',
                'cursor': cursor, 
            }
            
            res = session.get(
                'https://like.musinsa.com/api2/like/like-page/v1/tab/goods',
                params=params,
                headers=headers
            )

            time.sleep(1)


            for data in json.loads(res.text)['data']:
                if data['itemType'] != 'BANNERS':
                    if data['isSoldOut']:
                        continue
                    else :
                        price = data['price']
                        saleRate = str(data['saleRate']) + '%'
                        product_name = data['goodsName']
                        product_url = data['goodsLinkUrl']
                        print(product_name, saleRate, price, product_url)
                        product_list.append([product_name, saleRate, price, product_url])

            cursor = json.loads(res.text)['link']['nextCursor']
            if cursor is None:
                break
        driver.quit()
        
        path = "/opt/airflow/files"
        if not os.path.exists(path):
            os.system(f'mkdir -p {path}')
        df = pd.DataFrame(product_list) #columns = ['상품이름','세일률','가격','상품링크']
        df.to_csv(path + '/musinsa_products.csv', index=False, encoding='utf-8')

        sys.exit()

        

    py_t1 = PythonOperator(
        task_id='py_t1',
        python_callable=crawling_sale
    )

    py_t1