import streamlit as st
import pandas as pd
from huggingface_hub import InferenceClient
import os
from datetime import datetime
import io
from PIL import Image

# Streamlit 페이지 설정 - 밝은 테마
st.set_page_config(
    page_title="AI 아바타 생성기",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS - 밝은 테마
st.markdown("""
    <style>
        /* 밝은 배경색 */
        .stApp {
            background-color: #f8f9fa;
        }
        /* 카드 스타일 */
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        h1, h2, h3 {
            color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

# API 클라이언트 초기화
client = InferenceClient(
    provider="auto"
)

# 저장 디렉토리 생성
save_dir = "avatar_records"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 세션 상태 초기화
if "generated_avatar" not in st.session_state:
    st.session_state.generated_avatar = None
if "current_description" not in st.session_state:
    st.session_state.current_description = ""
if "current_user_name" not in st.session_state:
    st.session_state.current_user_name = ""

# 헤더
st.markdown("# 🎨 AI 아바타 생성기")
st.markdown("**당신을 표현하는 유니크한 캐릭터를 만들어보세요!**")
st.markdown("---")

# 메인 컨텐츠
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📝 아바타 설명")
    
    user_name = st.text_input(
        "이름",
        placeholder="예: 민지, Tom",
        key="input_name"
    )
    
    user_description = st.text_area(
        "본인을 자유롭게 설명해주세요",
        placeholder="예: 20대 여성, 긴 검은머리, 밝은 표정, 안경, 사랑스러운 느낌",
        height=120,
        key="input_description"
    )
    
    # 생성 버튼
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        generate_btn = st.button("✨ 아바타 생성", use_container_width=True, type="primary")
    
    with col_btn2:
        regenerate_btn = st.button("🔄 재생성", use_container_width=True)
    
    with col_btn3:
        reset_btn = st.button("🗑️ 초기화", use_container_width=True)
    
    # 생성 로직
    if generate_btn and user_description.strip():
        st.session_state.current_user_name = user_name if user_name else "Anonymous"
        st.session_state.current_description = user_description
        
        # 귀여운 스타일 프롬프트 생성
        cute_prompt = f"Cute adorable character illustration, lovely kawaii style: {user_description}. Bright colors, friendly expression, digital art, high quality"
        
        with st.spinner("🌟 아바타를 생성 중입니다..."):
            try:
                image = client.text_to_image(
                    cute_prompt,
                    model="black-forest-labs/FLUX.1-dev",
                )
                st.session_state.generated_avatar = image
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
    
    elif regenerate_btn and st.session_state.current_description:
        cute_prompt = f"Cute adorable character illustration, lovely kawaii style: {st.session_state.current_description}. Bright colors, friendly expression, digital art, high quality"
        
        with st.spinner("🌟 아바타를 재생성 중입니다..."):
            try:
                image = client.text_to_image(
                    cute_prompt,
                    model="black-forest-labs/FLUX.1-dev",
                )
                st.session_state.generated_avatar = image
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
    
    elif reset_btn:
        st.session_state.generated_avatar = None
        st.session_state.current_description = ""
        st.session_state.current_user_name = ""
        st.rerun()
    
    elif (generate_btn or regenerate_btn) and not user_description.strip():
        st.warning("⚠️ 설명을 입력해주세요!")

# 아바타 표시
with col2:
    st.markdown("## 🖼️ 생성된 아바타")
    
    if st.session_state.generated_avatar:
        st.image(st.session_state.generated_avatar, use_column_width=True)
        
        # 저장 버튼
        if st.button("💾 아바타 저장", use_container_width=True, key="save_btn"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            user_name_safe = st.session_state.current_user_name.replace(" ", "_")
            
            # JPG 이미지 저장
            image_path = f"{save_dir}/avatar_{timestamp}_{user_name_safe}.jpg"
            st.session_state.generated_avatar.save(image_path, "JPEG")
            
            # CSV에 메타데이터 저장
            csv_path = f"{save_dir}/avatar_records.csv"
            
            new_record = {
                "생성일시": timestamp,
                "이름": st.session_state.current_user_name,
                "설명": st.session_state.current_description,
                "이미지파일": image_path,
                "저장시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            else:
                df = pd.DataFrame([new_record])
            
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
            st.success(f"✅ 저장 완료!\n📁 {image_path}")
    else:
        st.info("🎨 아바타를 생성하면 여기에 표시됩니다")

# 사이드바 - 갤러리
st.markdown("---")
st.markdown("## 📚 갤러리")

# 생성된 아바타 목록 보기
csv_path = f"{save_dir}/avatar_records.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    st.markdown(f"**총 {len(df)}개의 아바타**")
    
    # 탭으로 표시
    tab1, tab2 = st.tabs(["📷 이미지 보기", "📊 목록 보기"])
    
    with tab1:
        # 이미지 갤러리
        if len(df) > 0:
            for idx, row in df.iterrows():
                if os.path.exists(row["이미지파일"]):
                    col_img1, col_img2 = st.columns([3, 1])
                    
                    with col_img1:
                        try:
                            img = Image.open(row["이미지파일"])
                            st.image(img, caption=f"{row['이름']} - {row['생성일시']}", use_column_width=True)
                            st.caption(f"설명: {row['설명'][:50]}...")
                        except:
                            st.warning(f"이미지를 열 수 없음: {row['이미지파일']}")
                    
                    with col_img2:
                        if st.button("📥", key=f"download_{idx}"):
                            with open(row["이미지파일"], "rb") as file:
                                st.download_button(
                                    label="다운로드",
                                    data=file,
                                    file_name=os.path.basename(row["이미지파일"]),
                                    mime="image/jpeg",
                                    key=f"dl_{idx}"
                                )
                    
                    st.divider()
    
    with tab2:
        # CSV 테이블 표시
        st.dataframe(df, use_container_width=True)
        
        # CSV 다운로드
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 CSV 전체 다운로드",
            data=csv_data,
            file_name=f"avatar_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # 전체 ZIP 다운로드 (옵션)
        if st.button("📦 모든 이미지 + CSV 다운로드", use_container_width=True):
            st.info("💡 모든 파일은 avatar_records 폴더에 저장되어 있습니다!")

else:
    st.info("아직 생성된 아바타가 없습니다. 위에서 아바타를 생성해보세요! ✨")

# 푸터
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🎨 AI 아바타 생성기 | Powered by FLUX.1-dev</p>
        <p style='font-size: 12px;'>생성된 이미지는 <code>avatar_records</code> 폴더에 저장됩니다.</p>
    </div>
""", unsafe_allow_html=True)
