from airflow import DAG
import pendulum
import datetime
from airflow.operators.python import PythonOperator
import random
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

with DAG(
    dag_id="dags_fashion_trend",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    def color_trend() :
        from configs.trend import trend
        import requests
        import cv2
        import numpy as np
        from sklearn.cluster import KMeans
        from collections import Counter

        df = trend()
        rgb_list = []

        for image in df['image'] :
            url = image
            response = requests.get(url)
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # (속도 개선을 위해 이미지 크기를 조정할 수 있음)
            resized_img = cv2.resize(img, (300, 300))
            height, width = resized_img.shape[:2]
            
            # 2. GrabCut을 이용해 옷(전경) 영역 추출
            mask = np.zeros((height, width), np.uint8)
            
            # GrabCut에서 사용할 임시 배열 (배경, 전경 모델)
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            
            # 옷 영역을 포함할 것으로 예상되는 사각형 (경우에 따라 조정 필요)
            rect = (int(width*0.1), int(height*0.1), int(width*0.8), int(height*0.8))
            
            # GrabCut 실행 (반복횟수 5회)
            cv2.grabCut(resized_img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            
            # mask에서 0,2는 배경, 1,3은 전경으로 구분됨
            # 전경(옷) 영역만 1로 만들어줌
            mask2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
            foreground = resized_img * mask2[:, :, np.newaxis]
            
            # 3. 전경(옷) 영역의 픽셀만 추출 (배경은 [0,0,0])
            clothing_pixels = foreground.reshape(-1, 3)
            clothing_pixels = clothing_pixels[np.any(clothing_pixels != [0, 0, 0], axis=1)]
            
            # 4. KMeans 클러스터링으로 대표 색상 추출 (옷 영역 내에서)
            k = 3  # 추출할 색상 군집 수 (원하는 값으로 조정 가능)
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(clothing_pixels)
            cluster_centers = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            
            # 각 군집의 픽셀 수 계산 후 가장 많은 군집 선택
            counts = Counter(labels)
            dominant_index = counts.most_common(1)[0][0]
            dominant_color = cluster_centers[dominant_index]
            
            rgb_list.append(dominant_color)

        
        rgb_list = [rgb.tolist() for rgb in rgb_list]
        
        return rgb_list

    
        

       
    def insert_color(postgres_conn_id, tbl_nm, **kwargs):
        postgres_hook = PostgresHook(postgres_conn_id)
        ti = kwargs['ti']
        rgb_list = ti.xcom_pull(task_ids='py_t1')

        delete_sql = f"DELETE FROM {tbl_nm}"
        postgres_hook.run(delete_sql)

        postgres_hook.insert_rows(table=tbl_nm, rows=rgb_list)

        
           

         
        

    py_t1 = PythonOperator(
        task_id='py_t1',
        python_callable=color_trend
    )


    insert_color_postgres = PythonOperator(
        task_id='insert_color_postgres',
        python_callable=insert_color,
        op_kwargs={
            'postgres_conn_id': 'deproject_sale_info',
            'tbl_nm': 'color_trend',
        }
    )

    py_t1 >> insert_color_postgres