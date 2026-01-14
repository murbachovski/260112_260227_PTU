from ultralytics import YOLO

# 1. 데이터셋 준비
# dataset/
# |- train/
#       |- Class1(person)/
#               |- class1.jpg
#               |- class1.jpg
#       |- Class2(dog)/
#               |- class2.jpg
#               |- class2.jpg
# |- val/
      # |- Class1(person)/
            # |- class1.jpg
            # |- class1.jpg
      # |- Class2(dog)/
            # |- class2.jpg
            # |- class2.jpg
# |- test/

# 1. 모델 로드
model = YOLO("yolo11n-cls.pt")

# 2. 모델 학습
model.train(
    data="dataset", # 데이터셋 경로
    epochs=2, # 학습 횟수
    batch=1, # 배치 사이즈
    imgsz=256, # 이미지 크기
)

# Happy, Sad, Normal 표정 분류 모델
# 이미지 크기 : 256
# 배치 사이즈 : free
# epochs : free
# *클래스별 이미지 수량은 통일

# 가장 우수한 성능 모델에 대해서 측정 후 시상
# 모델 완성 후 깃허브 업로드 후 링크 공유
# Chrome 웹 스토어 => Image Downloader 툴 활용
