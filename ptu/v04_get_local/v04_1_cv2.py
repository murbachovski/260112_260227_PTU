import cv2 # 컴퓨터 비전
import os # OS 접근 관련
from datetime import datetime # 날짜 관련

# 1. 저장 디렉토리 설정
save_dir = "./captured_images" # 사진을 저장할 폴더 경로
os.makedirs(save_dir, exist_ok=True) # 폴더가 없으면 생성

# 2. 카메라 연결
cap = cv2.VideoCapture(0)

# 3. 프레임 읽기
success, frame = cap.read()
if success:
    print("프레임 읽기 성공")
    
    # 현재 시간 기반 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(save_dir, f"result_{timestamp}.jpg")
    
    # 이미지 파일 저장
    cv2.imwrite(file_path, frame)
    print(f"사진이 저장 됐습니다. {file_path}")
else:
    print("프레임 읽기 실패")
    
# 4. 자원 해제
cap.release()
cv2.destroyAllWindows()