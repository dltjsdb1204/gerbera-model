import streamlit as st
import math
import matplotlib.pyplot as plt

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="거베라 생장 시뮬레이터", layout="wide")
st.title("🌿 거베라 줄기 생장 시뮬레이터")
st.markdown("환경 조건(빛, 규소)에 따른 거베라 줄기의 형태 변화를 예측합니다.")

# 2. 사이드바: 입력 변수
st.sidebar.header("📊 환경 변수 설정")
light_asymmetry = st.sidebar.slider("빛 비대칭성 (0~1)", 0.0, 1.0, 0.1, 0.05)
si_strength = st.sidebar.slider("규소 강성 계수 (1~10)", 1.0, 10.0, 2.0, 0.5)
elongation_rate = st.sidebar.number_input("일일 줄기 신장률 (cm)", 0.5, 5.0, 2.0)

# 3. 모델 계산 로직
def run_simulation(light, si, rate):
    x, y = [0], [0]
    current_angle = 90  # 수직(90도)에서 시작
    
    for i in range(50): 
        # 굴중성: 90도로 돌아가려는 힘
        restoration = (90 - current_angle) * 0.1
        # 굴광성: 빛 방향으로 휘어지는 힘
        bending = light * 20 
        
        # 강성을 분모로 나누어 각도 변화량 결정
        angle_change = (restoration + bending) / si
        current_angle += angle_change
        
        rad = math.radians(current_angle)
        new_x = x[-1] + rate * math.cos(rad)
        new_y = y[-1] + rate * math.sin(rad)
        
        x.append(new_x)
        y.append(new_y)
    return x, y

# 4. 메인 화면: 결과 출력
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 시뮬레이션 실행"):
        x_coords, y_coords = run_simulation(light_asymmetry, si_strength, elongation_rate)
        
        fig, ax = plt.subplots(figsize=(6, 8))
        ax.plot(x_coords, y_coords, color='#2E7D32', linewidth=4, label='Gerbera Stem')
        
        # 축 레이블 및 범위 설정
        ax.set_xlabel("가로 위치 (Horizontal, cm)")
        ax.set_ylabel("수직 높이 (Vertical, cm)")
        ax.set_xlim(-60, 60)
        ax.set_ylim(0, 120) # 요청하신 대로 120으로 조정
        ax.set_aspect('equal')
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend()
        
        st.pyplot(fig)
        
        # 분석 결과 리포트
        final_x = x_coords[-1]
        bending_dist = abs(final_x)
        st.info(f"💡 분석 결과: 줄기가 중심에서 약 {bending_dist:.1f}cm 휘어졌습니다.")

# 5. 하단 도움말 섹션 (이선유 님을 위한 가이드)
st.divider()
st.header("📖 사용자 측정 및 입력 가이드")

tab1, tab2, tab3 = st.tabs(["💡 빛 비대칭성", "🦾 규소 강성", "📏 줄기 신장률"])

with tab1:
    st.subheader("빛 비대칭성 (Light Asymmetry)")
    st.write("온실 내 광원이 한쪽으로 치우친 정도를 측정합니다.")
    st.info("**측정법:** 스마트폰 조도계 앱으로 '가장 밝은 방향'과 '가장 어두운 방향'의 광량을 재세요.")
    st.latex(r"Value = \frac{Max\,Light - Min\,Light}{Total\,Light}")
    st.caption("※ 값이 0에 가까우면 균일광, 1에 가까우면 극단적 편광입니다.")

with tab2:
    st.subheader("규소 강성 계수 (Si Strength)")
    st.write("규소 시비에 따른 줄기의 단단함(물리적 저항력)입니다.")
    st.info("**측정법:** 줄기 끝에 추(물병)를 달아 휘어지는 정도를 비교하거나, 손으로 눌렀을 때의 저항감을 수치화하세요.")
    st.write("- **1.0:** 규소 미시비 (연약함)")
    st.write("- **3.0 이상:** 규소 충분 시비 (대나무처럼 빳빳함)")

with tab3:
    st.subheader("줄기 신장률 (Elongation Rate)")
    st.write("하루 동안 줄기가 자라나는 길이입니다.")
    st.info("**측정법:** 줄기에 점을 찍고 24시간 뒤 늘어난 길이를 자로 측정하세요.")
    st.write(f"현재 설정된 신장률로 성장 시, 최종 높이는 약 {2.0 * 50:.0f}cm에 도달하게 설계되었습니다.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Lee Seon-yu. Horticultural Biotech.")
