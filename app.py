import streamlit as st
import hashlib

# ----------------------------------
# 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="Event Designer AI",
    page_icon="🎉",
    layout="wide"
)

# ----------------------------------
# 간단한 회원 데이터 저장
# Streamlit 세션 동안 유지
# ----------------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ----------------------------------
# 비밀번호 암호화 함수
# ----------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ----------------------------------
# 회원가입 함수
# ----------------------------------
def signup(username, password, password_check):
    if username == "" or password == "":
        return False, "아이디와 비밀번호를 모두 입력해주세요."

    if username in st.session_state.users:
        return False, "이미 사용 중인 아이디입니다."

    if password != password_check:
        return False, "비밀번호가 일치하지 않습니다."

    if len(password) < 4:
        return False, "비밀번호는 4자 이상 입력해주세요."

    st.session_state.users[username] = hash_password(password)

    return True, "회원가입이 완료되었습니다!"


# ----------------------------------
# 로그인 함수
# ----------------------------------
def login(username, password):
    if username not in st.session_state.users:
        return False, "존재하지 않는 아이디입니다."

    if st.session_state.users[username] != hash_password(password):
        return False, "비밀번호가 올바르지 않습니다."

    st.session_state.logged_in = True
    st.session_state.current_user = username

    return True, "로그인 성공!"


# ----------------------------------
# 행사장 추천 함수
# ----------------------------------
def recommend_event(
    event_type,
    people,
    duration,
    age_group,
    atmosphere,
    ticket_price,
    location_type
):

    # 행사장 크기 추천
    if people <= 30:
        venue_size = "소규모 행사장"
        area = "약 50~100㎡"
        seating = "소규모 테이블 또는 자유 좌석"
    elif people <= 100:
        venue_size = "중형 행사장"
        area = "약 150~300㎡"
        seating = "테이블 좌석과 중앙 활동 공간"
    elif people <= 300:
        venue_size = "대형 행사장"
        area = "약 400~800㎡"
        seating = "구역별 좌석 배치와 넓은 이동 통로"
    else:
        venue_size = "초대형 행사장"
        area = "800㎡ 이상"
        seating = "대규모 관람석 및 구역별 동선 설계"

    # 진행 시간 추천
    if duration <= 2:
        schedule = "입장 → 메인 프로그램 → 자유 관람 → 퇴장"
    elif duration <= 5:
        schedule = "입장 → 오프닝 → 메인 프로그램 → 휴식 → 체험/부대행사 → 마무리"
    else:
        schedule = "입장 → 오프닝 → 프로그램 1 → 휴식 → 프로그램 2 → 식사/체험 → 메인 이벤트 → 마무리"

    # 연령대 추천
    age_recommend = {
        "10대": "포토존, 체험 부스, SNS 공유 공간을 확대하는 것을 추천합니다.",
        "20대": "트렌디한 포토존과 자유로운 네트워킹 공간을 추천합니다.",
        "30대": "휴식 공간과 체험 공간의 균형 있는 배치를 추천합니다.",
        "40대": "편안한 좌석과 명확한 안내 동선을 추천합니다.",
        "50대 이상": "넓은 통로, 충분한 휴식 공간, 접근성 높은 좌석을 추천합니다.",
        "전 연령대": "연령별 휴식 공간과 다양한 체험 공간을 함께 구성하는 것을 추천합니다."
    }

    # 분위기 추천
    atmosphere_recommend = {
        "활기차고 신나는": "메인 무대 중심 + 음악 + LED 조명 + 포토존",
        "고급스럽고 세련된": "입구 안내 공간 + 고급 테이블 + 은은한 조명 + VIP 공간",
        "편안하고 따뜻한": "휴식 공간 + 부드러운 조명 + 카페형 좌석",
        "창의적이고 독특한": "테마별 체험존 + 인터랙티브 공간 + 독특한 포토존",
        "자연 친화적인": "친환경 소품 + 자연 소재 + 휴식 공간"
    }

    # 실내/실외 추천
    if location_type == "실내":
        location_recommend = (
            "냉난방과 조명을 활용하여 날씨의 영향을 최소화할 수 있습니다. "
            "입구, 안내 데스크, 메인 행사 공간, 휴식 공간을 구분해 배치하세요."
        )
    else:
        location_recommend = (
            "날씨 변화에 대비할 수 있도록 그늘막 또는 휴식 공간을 고려하세요. "
            "입구와 메인 공간 사이의 이동 동선을 넓게 확보하는 것을 추천합니다."
        )

    # 입장료 분석
    if ticket_price == 0:
        price_recommend = "무료 행사이므로 많은 참여자를 고려해 입장 및 퇴장 동선을 넓게 설계하는 것이 좋습니다."
    elif ticket_price < 10000:
        price_recommend = "부담이 적은 입장료이므로 체험형 부스와 참여형 프로그램을 강화하는 것을 추천합니다."
    elif ticket_price < 30000:
        price_recommend = "중간 수준의 입장료이므로 메인 프로그램과 부대시설의 균형을 고려하는 것이 좋습니다."
    else:
        price_recommend = "상대적으로 높은 입장료이므로 프리미엄 서비스, 휴식 공간 또는 특별 프로그램을 고려하세요."

    result = f"""
## 🎉 {event_type} 행사장 설계 결과

### 📌 기본 행사 정보
- **예상 인원:** {people:,}명
- **진행 시간:** {duration}시간
- **예상 연령대:** {age_group}
- **원하는 분위기:** {atmosphere}
- **예상 입장료:** {ticket_price:,}원
- **행사 장소:** {location_type}

---

### 🏢 추천 행사장 규모
- **추천 규모:** {venue_size}
- **권장 면적:** {area}
- **좌석 구성:** {seating}

---

### 🗺️ 추천 공간 구성

1. **입구 및 안내 데스크**
   - 참가자 확인 및 안내
   - 행사장 전체 지도 제공

2. **메인 행사 공간**
   - 무대 또는 핵심 프로그램 진행
   - 예상 인원에 맞는 좌석 배치

3. **체험 및 부대행사 공간**
   - 행사 유형에 맞는 체험 부스 구성
   - 참가자의 자유로운 이동이 가능하도록 배치

4. **휴식 공간**
   - 장시간 행사일 경우 충분한 좌석 제공
   - 음료 및 간단한 휴식 공간 구성

5. **포토존 / 기념 공간**
   - 행사 분위기에 맞는 디자인 적용
   - 참가자가 사진을 찍을 수 있는 공간 마련

---

### ⏰ 추천 진행 구조
{schedule}

---

### 👥 연령대에 따른 설계
{age_recommend.get(age_group)}

---

### ✨ 분위기 디자인
**추천 구성:**  
{atmosphere_recommend.get(atmosphere)}

---

### 🏠 장소 특성
{location_recommend}

---

### 💰 입장료 분석
{price_recommend}

---

### 🤖 AI 종합 추천

이번 행사는 **{people:,}명 규모의 {event_type}**으로 계획하는 것이 적절합니다.

특히 **{atmosphere} 분위기**를 중심으로 설계하고, 
참가자가 **입구 → 안내 → 메인 행사 → 체험 공간 → 휴식 공간 → 퇴장**의 순서로 
자연스럽게 이동할 수 있도록 동선을 구성하는 것을 추천합니다.
"""

    return result


# ==================================
# 로그인하지 않은 경우
# ==================================
if not st.session_state.logged_in:

    st.title("🎉 Event Designer AI")
    st.subheader("사용자의 니즈에 맞춰 최적의 행사장을 설계해드립니다!")

    tab1, tab2 = st.tabs(["🔐 로그인", "📝 회원가입"])

    # ------------------------------
    # 로그인
    # ------------------------------
    with tab1:
        st.subheader("로그인")

        login_username = st.text_input(
            "아이디",
            key="login_username"
        )

        login_password = st.text_input(
            "비밀번호",
            type="password",
            key="login_password"
        )

        if st.button("로그인", use_container_width=True):
            success, message = login(
                login_username,
                login_password
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    # ------------------------------
    # 회원가입
    # ------------------------------
    with tab2:
        st.subheader("회원가입")

        new_username = st.text_input(
            "새 아이디",
            key="new_username"
        )

        new_password = st.text_input(
            "새 비밀번호",
            type="password",
            key="new_password"
        )

        password_check = st.text_input(
            "비밀번호 확인",
            type="password",
            key="password_check"
        )

        if st.button("회원가입", use_container_width=True):
            success, message = signup(
                new_username,
                new_password,
                password_check
            )

            if success:
                st.success(message)
                st.info("이제 로그인 탭에서 로그인해주세요!")
            else:
                st.error(message)


# ==================================
# 로그인 후 메인 화면
# ==================================
else:

    st.sidebar.title("🎉 Event Designer AI")
    st.sidebar.success(
        f"👤 {st.session_state.current_user}님 로그인 중"
    )

    if st.sidebar.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    st.title("🎪 AI 행사장 설계 서비스")
    st.write(
        "원하는 행사 정보를 입력하면 AI가 행사장 규모와 공간 구성을 추천합니다."
    )

    st.divider()

    # ------------------------------
    # 입력 폼
    # ------------------------------
    with st.form("event_form"):

        st.subheader("📝 행사 정보 입력")

        col1, col2 = st.columns(2)

        with col1:
            event_type = st.selectbox(
                "행사장의 유형",
                [
                    "공연",
                    "전시회",
                    "축제",
                    "박람회",
                    "강연",
                    "세미나",
                    "결혼식",
                    "파티",
                    "체험 행사",
                    "기타"
                ]
            )

            people = st.number_input(
                "예상 인원 수",
                min_value=1,
                max_value=100000,
                value=100,
                step=10
            )

            duration = st.number_input(
                "진행 시간 (시간)",
                min_value=1,
                max_value=24,
                value=3,
                step=1
            )

            age_group = st.selectbox(
                "예상 연령대",
                [
                    "10대",
                    "20대",
                    "30대",
                    "40대",
                    "50대 이상",
                    "전 연령대"
                ]
            )

        with col2:
            atmosphere = st.selectbox(
                "원하는 분위기",
                [
                    "활기차고 신나는",
                    "고급스럽고 세련된",
                    "편안하고 따뜻한",
                    "창의적이고 독특한",
                    "자연 친화적인"
                ]
            )

            ticket_price = st.number_input(
                "예상 입장료 (원)",
                min_value=0,
                max_value=1000000,
                value=10000,
                step=1000
            )

            location_type = st.radio(
                "실내 / 실외 선택",
                ["실내", "실외"],
                horizontal=True
            )

        submitted = st.form_submit_button(
            "✨ 나에게 맞는 행사장 설계하기",
            use_container_width=True
        )

    # ------------------------------
    # 결과 출력
    # ------------------------------
    if submitted:

        st.divider()

        with st.spinner("AI가 행사장을 설계하고 있습니다..."):
            result = recommend_event(
                event_type,
                people,
                duration,
                age_group,
                atmosphere,
                ticket_price,
                location_type
            )

        st.success("행사장 설계가 완료되었습니다!")

        st.markdown(result)

        st.info(
            "💡 이 결과를 바탕으로 실제 행사장의 공간 배치와 프로그램을 구체적으로 계획할 수 있습니다."
        )
