import streamlit as st
import math
import matplotlib.pyplot as plt

# 페이지 제목
st.title("🌿 거베라 줄기 생장 시뮬레이터")
st.markdown("환경 조건에 따른 거베라 줄기의 휘어짐을 시뮬레이션합니다.")

# 사이드바 설정 (환경 조건 입력)
st.sidebar.header("환경 변수 설정")
light_asymmetry = st.sidebar.slider("빛 비대칭성 (Light Asymmetry)", 0.0, 1.0, 0.1, 0.05)
si_strength = st.sidebar.slider("규소 강성 계수 (Si Strength)", 1.0, 10.0, 2.0, 0.5)
elongation_rate = st.sidebar.number_input("줄기 신장률", 1.0, 5.0, 2.0)

# 모델 계산 로직 (기존 선유 님의 모델 기반)
def run_simulation(light, si, rate):
    x, y = [0], [0]
    current_angle = 90  # 수직 시작
    
    for i in range(50): # 50단계 성장
        # 1. 굴중성 (수직으로 돌아가려는 힘)
        restoration = (90 - current_angle) * 0.1
        # 2. 굴광성 (빛 방향으로 휘어지는 힘)
        bending = light * 20 
        
        # 3. 강성 반영하여 각도 변화 계산
        angle_change = (restoration + bending) / si
        current_angle += angle_change
        
        # 4. 좌표 계산
        rad = math.radians(current_angle)
        new_x = x[-1] + rate * math.cos(rad)
        new_y = y[-1] + rate * math.sin(rad)
        
        x.append(new_x)
        y.append(new_y)
    return x, y

# 시뮬레이션 실행 및 시각화
if st.button("시뮬레이션 실행"):
    x_coords, y_coords = run_simulation(light_asymmetry, si_strength, elongation_rate)
    
    fig, ax = plt.subplots()
    ax.plot(x_coords, y_coords, color='green', linewidth=3, label='Gerbera Stem')
    ax.set_xlim(-50, 50)
    ax.set_ylim(0, 150)
    ax.set_aspect('equal')
    ax.legend()
    st.pyplot(fig)
    
    # 분석 결과 메시지
    final_angle = math.degrees(math.atan2(y_coords[-1], x_coords[-1]))
    st.info(f"분석 결과: 최종 굽힘 각도는 약 {90 - int(final_angle)}도 입니다.")
