from PIL import Image, ImageEnhance, ImageOps
import matplotlib.pyplot as plt

# 1. 이미지 로드
img = Image.open("captured_images/result_20260113_154745.jpg")

# 2. 이미지 전처리
img_rotated = img.rotate(90)

# 2-1. 이미지 전처리(밝기 조절)
# 2-2. 이미지 전처리(좌우 반전)

# 3. 결과 시각화
fig, ax = plt.subplots(2, 3, figsize=(20, 10))

# 원본 이미지
ax[0,0].imshow(img)
ax[0,0].axis('off')
ax[0,0].set_title("Original")

# 회전 이미지
ax[0,1].imshow(img_rotated)
ax[0,1].axis('off')
ax[0,1].set_title("Rotated 90도")

# + 밝기 이미지
# + 좌우 반전 이미지

plt.show()

img_rotated.save("./img_rotated.jpg")
# + 밝기 이미지 저장
# + 좌우 반전 이미지 저장

print("이미지 저장이 잘 됐습니다.")
