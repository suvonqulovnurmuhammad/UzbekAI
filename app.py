
import streamlit as st
from google import genai
from datetime import datetime
from zoneinfo import ZoneInfo
import html

# ==============================
# 1. ASOSIY SOZLAMALAR
# ==============================

st.set_page_config(
    page_title="UzbekAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = """
Sen UzbekAI nomli aqlli yordamchisan.

ASOSIY QOIDALAR:
- Foydalanuvchiga asosan o'zbek tilida javob ber.
- Muloyim, aniq va tushunarli yoz.
- Savolga to'g'ridan-to'g'ri javob ber.
- Kod so'ralsa, ishlatishga tayyor kod yoz.
- Matematik masalalarni bosqichma-bosqich tushuntir.
- Bilmagan ma'lumotingni to'qib chiqarma.
- Foydalanuvchi boshqa tilda so'rasa, o'sha tilda javob berishing mumkin.

SANA VA YANGI MA'LUMOTLAR:
- Bugungi sana haqidagi maxsus ko'rsatmaga amal qil.
- 2025 yoki 2026-yil haqida so'ralganda, buni avtomatik
  ravishda kelajak deb hisoblama.
- Hozir sodir bo'layotgan yoki yaqinda sodir bo'lgan
  voqealar haqida Google Search orqali qidir.
- Sport natijalari, yangiliklar, texnologiyalar va joriy
  ma'lumotlarni imkon qadar ishonchli manbalardan tekshir.
- Qidiruv natijasi topilmasa, buni ochiq ayt.
- Eski bilimlaringni yangi tasdiqlangan ma'lumot sifatida ko'rsatma.
- Javobda kerak bo'lsa, manbalarni ko'rsat.
"""


def get_current_date():
    return datetime.now(
        ZoneInfo("Asia/Tashkent")
    ).strftime("%d-%m-%Y")


# ==============================
# 2. API KALITINI OLISH
# ==============================

def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        return key.strip() if key else ""
    except Exception:
        return ""


api_key = get_api_key()


# ==============================
# 3. DIZAYN
# ==============================

st.markdown(
    """
    <style>
    .stApp {
        background: #0b1020;
        color: #f4f6ff;
    }

    [data-testid="stSidebar"] {
        background: #11182b;
        border-right: 1px solid #26314a;
    }

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #8b9dff;
        margin-top: 10px;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #aab5d1;
        font-size: 17px;
        margin-bottom: 28px;
    }

    .info-card {
        background: #141d33;
        border: 1px solid #283653;
        border-radius: 14px;
        padding: 16px;
        margin: 10px 0;
    }

    div[data-testid="stChatMessage"] {
        background: #121a2d;
        border: 1px solid #26314a;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 10px;
    }

    div[data-testid="stChatInput"] {
        border-color: #5367c9;
    }

    .small-note {
        color: #9caac8;
        font-size: 12px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================
# 4. CHAT TARIXI
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None


# ==============================
# 5. CHAP MENYU
# ==============================

with st.sidebar:
    st.markdown("## 🤖 UzbekAI")
    st.caption("Sening aqlli AI yordamching")

    st.divider()

    st.markdown("### 💬 Suhbat")

    if st.button("＋ Yangi suhbat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.previous_interaction_id = None
        st.rerun()

    st.markdown(
        f"""
        <div class="info-card">
            <b>📅 Bugungi sana</b><br>
            {get_current_date()}<br><br>
            <b>🧠 Model</b><br>
            {MODEL}<br><br>
            <b>🌐 Internet qidiruvi</b><br>
            Google Search
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("UzbekAI • AI yordamchi")


# ==============================
# 6. ASOSIY OYNA
# ==============================

st.markdown(
    '<div class="main-title">UzbekAI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Sening aqlli AI yordamching</div>',
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown(
        """
        <div class="info-card">
            <h3>Assalomu alaykum! 👋</h3>
            Men UzbekAI yordamchisiman.
            <br><br>
            Menga savol ber, masala yech, kod yozdir
            yoki yangi ma'lumotlarni qidir.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Avvalgi xabarlarni ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==============================
# 7. FOYDALANUVCHI XABARI
# ==============================

user_message = st.chat_input(
    "UzbekAI'ga xabar yoz..."
)

if user_message:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # API kaliti tekshiruvi
    if not api_key:
        error_message = (
            "API kaliti topilmadi. Streamlit Cloud'da "
            "Settings → Secrets bo'limiga kirib, "
            "GEMINI_API_KEY kalitini sozla."
        )

        with st.chat_message("assistant"):
            st.error(error_message)

    else:
        try:
            client = genai.Client(api_key=api_key)

            current_date = get_current_date()

            instructions = f"""
{SYSTEM_PROMPT}

BUGUNGI SANA:
{current_date} (O'zbekiston vaqti, Asia/Tashkent).

Agar foydalanuvchi bugungi sana yoki yilni so'rasa,
yuqoridagi sanadan foydalan.

Agar foydalanuvchi yangi ma'lumot so'rasa,
Google Search vositasidan foydalanib tekshir.
"""

            with st.chat_message("assistant"):
                with st.spinner(
                    "UzbekAI javob tayyorlamoqda..."
                ):
                    request_args = {
                        "model": MODEL,
                        "input": user_message,
                        "system_instruction": instructions,
                        "tools": [
                            {"type": "google_search"}
                        ],
                    }

                    previous_id = (
                        st.session_state.previous_interaction_id
                    )

                    if previous_id:
                        request_args[
                            "previous_interaction_id"
                        ] = previous_id

                    response = client.interactions.create(
                        **request_args
                    )

                    answer = (
                        getattr(response, "output_text", None)
                        or ""
                    ).strip()

                    if not answer:
                        answer = (
                            "Javob matni kelmadi. "
                            "Iltimos, qaytadan urinib ko'r."
                        )

                    st.markdown(answer)

                    # Suhbat kontekstini saqlash
                    new_id = getattr(response, "id", None)

                    if new_id:
                        st.session_state.previous_interaction_id = (
                            new_id
                        )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

            try:
                client.close()
            except Exception:
                pass

        except Exception as error:
            error_text = str(error)

            with st.chat_message("assistant"):
                st.error(
                    "UzbekAI javob berishda xatoga uchradi."
                )

                with st.expander("Xatolik tafsiloti"):
                    st.code(error_text)

            # Oldingi xatodan keyin keyingi xabarni
            # yangi suhbat sifatida yuborish
            st.session_state.previous_interaction_id = None
