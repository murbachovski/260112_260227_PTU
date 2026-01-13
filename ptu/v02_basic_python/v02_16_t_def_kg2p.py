# kg to pound 변환하는 함수 실습
import streamlit as st

# 1. 함수 정의
def meters_to_feet(meters):
    return meters * 3.28084

# 2. 웹 UI 제목
st.title("📏 미터(m) ➡️ 피트(ft) 변환기")
st.write("미터 값을 입력하면 피트(ft)로 즉시 변환해 드립니다.")

# 3. 사용자 입력 (웹 페이지의 입력 칸)
meters = st.number_input("미터(m) 값을 입력하세요:", min_value=0.0, format="%.2f")

# 4. 결과 출력
if st.button("변환하기"):
    feet = meters_to_feet(meters)
    st.success(f"결과: {meters}m는 **{feet:.2f}ft**입니다.")