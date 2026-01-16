import cv2
import numpy as np
from ultralytics import YOLO
import time
from collections import deque
from openvino.runtime import Core

# 1. 모델 로드
print("모델 로딩 중...")
model_pt = YOLO("yolo11n.pt")

# OpenVINO 모델 로드
ie = Core()
openvino_model = ie.read_model(model="yolo11n_openvino_model/yolo11n.xml")
compiled_model = ie.compile_model(openvino_model, device_name="CPU")

print("모델 로드 완료")

# 2. RTSP 스트림 설정
rtsp_url = "http://210.99.70.120:1935/live/cctv013.stream/playlist.m3u8"
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print(f"스트림을 열 수 없습니다: {rtsp_url}")
    exit()

print("스트림 연결 완료")

# FPS 계산용 변수
fps_pt_deque = deque(maxlen=30)  # 최근 30프레임 FPS
fps_openvino_deque = deque(maxlen=30)

# 3. 메인 루프
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다. 재연결 중...")
            cap = cv2.VideoCapture(rtsp_url)
            continue

        frame_resized = cv2.resize(frame, (640, 480))

        # PT 모델 추론
        start_time_pt = time.time()
        results_pt = model_pt(frame_resized, device='cpu', verbose=False)
        time_pt = time.time() - start_time_pt
        fps_pt = 1 / time_pt if time_pt > 0 else 0
        fps_pt_deque.append(fps_pt)
        avg_fps_pt = np.mean(fps_pt_deque)

        # OpenVINO 모델 추론
        start_time_openvino = time.time()
        # 이미지 전처리 (YOLO 방식)
        img_resized = cv2.resize(frame_resized, (640, 640))
        img_normalized = img_resized.astype(np.float32) / 255.0
        img_transposed = np.transpose(img_normalized, (2, 0, 1))
        img_batched = np.expand_dims(img_transposed, 0)
        
        # OpenVINO 추론
        infer_request = compiled_model.create_infer_request()
        infer_request.infer({0: img_batched})
        output = infer_request.get_output_tensor(0).data
        
        time_openvino = time.time() - start_time_openvino
        fps_openvino = 1 / time_openvino if time_openvino > 0 else 0
        fps_openvino_deque.append(fps_openvino)
        avg_fps_openvino = np.mean(fps_openvino_deque)

        # 결과 이미지 생성
        frame_pt = results_pt[0].plot()
        frame_openvino = frame_resized.copy()  # OpenVINO는 결과 시각화 없이 FPS만 표시

        # FPS 텍스트 추가
        cv2.putText(frame_pt, f"PT FPS: {avg_fps_pt:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_pt, f"Time: {time_pt*1000:.2f}ms", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(frame_openvino, f"OpenVINO FPS: {avg_fps_openvino:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame_openvino, f"Time: {time_openvino*1000:.2f}ms", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # 콘솔 출력 (매 30프레임마다)
        frame_count = len(fps_pt_deque)
        if frame_count % 30 == 0:
            print(f"\n[Frame {frame_count}]")
            print(f"PT Model    - FPS: {avg_fps_pt:.2f}, Time: {time_pt*1000:.2f}ms")
            print(f"OpenVINO Model - FPS: {avg_fps_openvino:.2f}, Time: {time_openvino*1000:.2f}ms")
            print(f"속도 향상: {(time_pt/time_openvino - 1)*100:.2f}%" if time_openvino > 0 else "")

        # 윈도우 표시
        cv2.imshow("YOLO PT Model", frame_pt)
        cv2.imshow("YOLO OpenVINO Model", frame_openvino)

        # 종료 키 (q)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n프로그램을 종료합니다.")
            break

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")

finally:
    cap.release()
    cv2.destroyAllWindows()

    # 최종 결과 출력
    if fps_pt_deque and fps_openvino_deque:
        final_avg_fps_pt = np.mean(fps_pt_deque)
        final_avg_fps_openvino = np.mean(fps_openvino_deque)
        print(f"\n=== 최종 결과 ===")
        print(f"PT Model 평균 FPS: {final_avg_fps_pt:.2f}")
        print(f"OpenVINO Model 평균 FPS: {final_avg_fps_openvino:.2f}")
        if final_avg_fps_openvino > 0:
            speed_improvement = (final_avg_fps_openvino / final_avg_fps_pt - 1) * 100
            print(f"성능 향상: {speed_improvement:.2f}%")
