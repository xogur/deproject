from airflow import DAG
import pendulum
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd


def insert_user_product_like(**kwargs):
    dag_run = kwargs.get("dag_run")
    if not dag_run:
        print("❌ dag_run이 전달되지 않았습니다.")
        return

    user_email = dag_run.conf.get("user_email")
    print("✅ 전달받은 무신사 ID:", user_email)

    path = "/opt/airflow/files/musinsa_products.csv"
    df = pd.read_csv(path, skiprows=1, header=None, names=['product_name', 'sale', 'price', 'product_link'])

    postgres_hook = PostgresHook(postgres_conn_id='deproject_sale_info')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        product_name, sale, price, product_link = row

        # 상품이 존재하지 않으면 먼저 sale_info에 삽입
        insert_sale_info_sql = """
            INSERT INTO sale_info (product_link, product_name, sale, price)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (product_link) DO NOTHING
        """
        cursor.execute(insert_sale_info_sql, (product_link, product_name, sale, price))

        # user_product_like에 유저와 상품 링크를 추가
        insert_like_sql = """
            INSERT INTO user_product_like (user_email, product_link)
            VALUES (%s, %s)
            ON CONFLICT (user_email, product_link) DO NOTHING
        """
        cursor.execute(insert_like_sql, (user_email, product_link))

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    dag_id="dags_user_product_like",
    start_date=pendulum.datetime(2023, 4, 1, tz="Asia/Seoul"),
    schedule=None,
    catchup=False,
    tags=["musinsa", "user"]
) as dag:

    insert_like_task = PythonOperator(
        task_id="insert_like_task",
        python_callable=insert_user_product_like,
        provide_context=True
    )

insert_like_task