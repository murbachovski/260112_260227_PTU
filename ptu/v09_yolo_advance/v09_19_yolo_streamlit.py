from ultralytics import solutions

# 1. Infrence 객체 생성
inf = solutions.Inference(
    model="yolo11n.pt"
)

# 2. 추론 실행
inf.inference()
# pip install streamlit
# streamlit run ./v09_19_yolo_streamlit.py