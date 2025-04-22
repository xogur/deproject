from airflow import DAG
import pendulum
import datetime
from airflow.operators.python import PythonOperator
import random
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

with DAG(
    dag_id="dags_fashion_item_trend_load",
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2023, 3, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    def insert_trend_item(postgres_conn_id, tbl_nm, **kwargs):
        from configs.trend import trend
        dag_run = kwargs['dag_run']
        style  = dag_run.conf.get('style')
        season = dag_run.conf.get('season')
        gender = dag_run.conf.get('gender')

        df = trend()
        df = df.astype(object)

        print(style, season, gender)

        # df를 리스트의 튜플 형태로 변환
        data = [tuple(row) for row in df.to_records(index=False)]

        # PostgresHook 연결
        postgres_hook = PostgresHook(postgres_conn_id)

        # 테이블 비우기 (선택사항)
        delete_sql = f"DELETE FROM {tbl_nm}"
        postgres_hook.run(delete_sql)

        # 데이터 삽입
        postgres_hook.insert_rows(table=tbl_nm, rows=data)

        
           

         

    insert_trendItem_postgres = PythonOperator(
        task_id='insert_trendItem_postgres',
        python_callable=insert_trend_item,
        op_kwargs={
            'postgres_conn_id': 'deproject_sale_info',
            'tbl_nm': 'item_trend',
        }
    )

    insert_trendItem_postgres