from airflow import DAG
import pendulum
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

with DAG(
        dag_id='dags_sale_load',
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        schedule='0 7 * * *',
        catchup=False
) as dag:
    def insert_dataframe(postgres_conn_id, tbl_nm, file_path, **kwargs):
        import pandas as pd
        # CSV 읽기 (헤더 없음이므로 직접 컬럼 지정)
        df = pd.read_csv(file_path, header=None, names=['product_name', 'sale', 'price', 'product_link'])

        # DataFrame을 리스트로 변환
        records = df.values.tolist()

        # PostgreSQL 연결 및 적재
        postgres_hook = PostgresHook(postgres_conn_id)
        postgres_hook.insert_rows(table=tbl_nm, rows=records)

    insrt_postgres = PythonOperator(
        task_id='insrt_postgres',
        python_callable=insert_dataframe,
        op_kwargs={
            'postgres_conn_id': 'deproject_sale_info',
            'tbl_nm': 'sale_info',
            'file_path': '/opt/airflow/files/musinsa_products.csv'  # 경로는 환경에 맞게
        }
    )