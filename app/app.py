import streamlit as st
import pandas as pd
import psycopg2

# DB 연결
conn = psycopg2.connect(
    host="postgres_custom",
    database="deproject",
    user="xogur",
    password="xogur",
    port="5432"
)

# 쿼리 예시
query = "SELECT r, g, b, image FROM color_trend LIMIT 10;"
df = pd.read_sql(query, conn)

# 시각화
st.title("🎨 최근 유행 색상 분석")
st.write("RGB 및 관련 이미지:")
st.dataframe(df)