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

# -------------------------
# 📂 파일 업로드 기능
# -------------------------
st.subheader("📂 파일 업로드 변환")

uploaded_file = st.file_uploader("CSV 파일 업로드 (예: '섭씨' 또는 '화씨' 컬럼 포함)", type=["csv"])

if uploaded_file is not None:
    file_df = pd.read_csv(uploaded_file)

    st.write("업로드된 데이터 미리보기:")
    st.dataframe(file_df.head())

    try:
        if conversion == "섭씨 → 화씨" and "섭씨" in file_df.columns:
            file_df["화씨"] = file_df["섭씨"].apply(c_to_f)

        elif conversion == "화씨 → 섭씨" and "화씨" in file_df.columns:
            file_df["섭씨"] = file_df["화씨"].apply(f_to_c)

        elif conversion == "섭씨 → 켈빈" and "섭씨" in file_df.columns:
            file_df["켈빈"] = file_df["섭씨"].apply(c_to_k)

        elif conversion == "켈빈 → 섭씨" and "켈빈" in file_df.columns:
            file_df["섭씨"] = file_df["켈빈"].apply(k_to_c)

        else:
            st.warning("⚠️ CSV에 변환에 필요한 컬럼명이 없습니다. (예: '섭씨', '화씨', '켈빈')")

        st.write("✅ 변환된 데이터:")
        st.dataframe(file_df)

        # 변환된 파일 다운로드
        csv = file_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 변환된 CSV 다운로드",
            data=csv,
            file_name="converted_temperature.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"오류 발생: {e}")

# 푸터
st.markdown("---")
st.caption("✨ Made with Streamlit · 온도 변환기 by HJ")
