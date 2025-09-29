import streamlit as st
import pandas as pd

st.set_page_config(page_title="🌡️ 온도 변환기", page_icon="🔥", layout="centered")

st.title("🌡️ 온도 변환기")

# 입력 섹션
with st.container():
    st.markdown("### ✍️ 입력")
    temp_input = st.number_input("변환할 온도를 입력하세요", value=0.0, step=0.1)
    conversion = st.radio(
        "변환 방향 선택",
        ("섭씨 → 화씨", "화씨 → 섭씨", "섭씨 → 켈빈", "켈빈 → 섭씨"),
        horizontal=True
    )

# 변환 함수
def c_to_f(c): return c * 9/5 + 32
def f_to_c(f): return (f - 32) * 5/9
def c_to_k(c): return c + 273.15
def k_to_c(k): return k - 273.15

# 결과 카드
with st.container():
    st.markdown("### 📌 변환 결과")
    if conversion == "섭씨 → 화씨":
        result = c_to_f(temp_input)
        st.markdown(
            f"""
            <div style="background-color:#FFEECC;padding:20px;border-radius:15px;text-align:center;">
                <h3>🔥 {temp_input:.2f} ℃ → {result:.2f} ℉</h3>
            </div>
            """, unsafe_allow_html=True)

    elif conversion == "화씨 → 섭씨":
        result = f_to_c(temp_input)
        st.markdown(
            f"""
            <div style="background-color:#CCE5FF;padding:20px;border-radius:15px;text-align:center;">
                <h3>❄️ {temp_input:.2f} ℉ → {result:.2f} ℃</h3>
            </div>
            """, unsafe_allow_html=True)

    elif conversion == "섭씨 → 켈빈":
        result = c_to_k(temp_input)
        st.markdown(
            f"""
            <div style="background-color:#E6FFCC;padding:20px;border-radius:15px;text-align:center;">
                <h3>🧪 {temp_input:.2f} ℃ → {result:.2f} K</h3>
            </div>
            """, unsafe_allow_html=True)

    elif conversion == "켈빈 → 섭씨":
        result = k_to_c(temp_input)
        st.markdown(
            f"""
            <div style="background-color:#FFD6E6;padding:20px;border-radius:15px;text-align:center;">
                <h3>🌙 {temp_input:.2f} K → {result:.2f} ℃</h3>
            </div>
            """, unsafe_allow_html=True)

# 추가 기능: 변환 테이블
with st.expander("📊 변환 테이블 보기 (섭씨 -20℃ ~ 40℃ → 화씨)"):
    data = {"섭씨(℃)": list(range(-20, 41, 5))}
    data["화씨(℉)"] = [c_to_f(c) for c in data["섭씨(℃)"]]
    df = pd.DataFrame(data)
    st.table(df)

# 푸터
st.markdown("---")
st.caption("✨ Made with Streamlit · 온도 변환기 by HJ")
