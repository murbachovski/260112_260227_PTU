from ultralytics import FastSAM
import cv2

# 1. 이미지 경로
source = "v09_yolo_advance/dog1.jpg"

# 2. 모델 로드
model = FastSAM("FastSAM-s.pt")

# 3. 텍스트 기반 탐지
results = model(source, texts="dog")

# 4. 결과 이미지 저장
output_image = results[0].plot()
cv2.imwrite("output_result.jpg", output_image)
print(f"결과 이미지가 저장 됐습니다.{output_image}")