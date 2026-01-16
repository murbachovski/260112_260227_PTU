from ultralytics import solutions

# 1. SearchAPP 생성
app = solutions.SearchApp(
    device="cpu"
)

# 2. 앱 실행
app.run(debug=True)