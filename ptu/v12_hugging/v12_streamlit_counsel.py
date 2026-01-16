import streamlit as st
import pandas as pd
from huggingface_hub import InferenceClient
import os
from datetime import datetime
import csv

# Streamlit 페이지 설정
st.set_page_config(page_title="고민 상담", layout="wide")

# API 클라이언트 초기화
client = InferenceClient(
    provider="auto"
)

# 저장 디렉토리 생성
save_dir = "counseling_records"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "session_started" not in st.session_state:
    st.session_state.session_started = False

# 제목
st.title("💬 AI 고민 상담")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("상담 정보")
    user_name = st.text_input("이름을 입력해주세요:", value=st.session_state.user_name)
    
    if user_name:
        st.session_state.user_name = user_name
        st.session_state.session_started = True
    
    st.markdown("---")
    
    if st.session_state.messages:
        st.subheader("대화 내역")
        st.write(f"총 {len(st.session_state.messages)//2 if len(st.session_state.messages) > 0 else 0} 개의 상담")
        
        # CSV로 저장 버튼
        if st.button("💾 대화 내역 저장"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{save_dir}/counseling_{timestamp}_{user_name}.csv"
            
            # DataFrame 생성
            data = []
            for i, msg in enumerate(st.session_state.messages):
                data.append({
                    "순서": i + 1,
                    "역할": msg["role"],
                    "내용": msg["content"],
                    "시간": msg.get("time", "")
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            st.success(f"✅ 저장 완료: {filename}")
        
        # 다운로드 버튼
        if st.button("📥 CSV 다운로드"):
            data = []
            for i, msg in enumerate(st.session_state.messages):
                data.append({
                    "순서": i + 1,
                    "역할": msg["role"],
                    "내용": msg["content"],
                    "시간": msg.get("time", "")
                })
            
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False, encoding='utf-8-sig')
            
            st.download_button(
                label="📋 CSV 파일 다운로드",
                data=csv_data,
                file_name=f"counseling_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_name}.csv",
                mime="text/csv"
            )
        
        # 초기화 버튼
        if st.button("🔄 상담 초기화"):
            st.session_state.messages = []
            st.session_state.session_started = False
            st.rerun()

# 메인 화면
if st.session_state.session_started:
    # 채팅 영역
    chat_container = st.container()
    
    # 메시지 표시
    for message in st.session_state.messages:
        with chat_container:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(message["content"])
    
    # 입력 영역
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("고민을 말씀해주세요:", key="input")
    
    with col2:
        send_button = st.button("전송", use_container_width=True)
    
    # 전송 처리
    if send_button and user_input.strip():
        # 사용자 메시지 추가
        current_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": current_time
        })
        
        # 로딩 표시
        with st.spinner("상담사가 답변을 준비 중입니다..."):
            try:
                # DeepSeek API 호출
                completion = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3.2:novita",
                    messages=[
                        {
                            "role": "system",
                            "content": "당신은 따뜻하고 공감하는 고민 상담사입니다. 상대방의 고민을 잘 들어주고, 위로하고, 긍정적인 조언을 제공해주세요."
                        },
                        *[
                            {
                                "role": msg["role"],
                                "content": msg["content"]
                            }
                            for msg in st.session_state.messages
                        ]
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                # AI 답변 추가
                ai_response = completion.choices[0].message.content
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                
                st.rerun()
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
else:
    st.info("👈 왼쪽 사이드바에서 이름을 입력하고 시작해주세요.")
