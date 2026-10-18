
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="UzbekAI",
    page_icon="🇺🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== DIZAYN =====

st.markdown("""
<style>
.stApp {
    background: #101218 !important;
    color: #F1F5F9 !important;
}

header[data-testid="stHeader"] {
    background: #101218 !important;
}

section[data-testid="stSidebar"] {
    background: #171A22 !important;
    border-right: 1px solid #343A49 !important;
}

/* Xabar yozish maydoni */
.stChatInput,
div[data-testid="stChatInput"] {
    background: #202530 !important;
    border: 1px solid #4B5568 !important;
    border-radius: 16px !important;
}

.stChatInput textarea,
div[data-testid="stChatInput"] textarea {
    color: #000000  !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #68E0CF !important;
    background: transparent !important;
}

.stChatInput textarea::placeholder,
div[data-testid="stChatInput"] textarea::placeholder {
    color: #B8C1D1 !important;
    -webkit-text-fill-color: #B8C1D1 !important;
    opacity: 1 !important;
}

/* Yon panelni ochish-yopish tugmalari */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"] {
    color: #FFFFFF !important;
    background: #252B37 !important;
    opacity: 1 !important;
}

[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg,
button[kind="header"] svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* Suhbat xabarlari */
div[data-testid="stChatMessage"] {
    background: #191D27 !important;
    color: #F1F5F9 !important;
    border: 1px solid #303746 !important;
    border-radius: 16px !important;
}

div[data-testid="stChatMessage"] p {
    color: #F1F5F9 !important;
}

/* Tugmalar */
.stButton > button {
    background: #202530 !important;
    color: #FFFFFF !important;
    border: 1px solid #41495A !important;
    border-radius: 12px !important;
}

.stButton > button:hover {
    border-color: #68E0CF !important;
    color: #68E0CF !important;
}

/* Oddiy matnlar */
.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3 {
    color: #F1F5F9;
}
</style>
""", unsafe_allow_html=True)


# ===== SOZLAMALAR =====
MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = """
Sen UzbekAI nomli foydali va samimiy AI yordamchisan.
Foydalanuvchiga asosan o'zbek tilida javob ber.
Savollarni aniq, tushunarli va tartibli izohla.
Kerak bo'lsa, misollar va bosqichma-bosqich ko'rsatmalar ber.
Agar foydalanuvchi boshqa tilda so'rasa, o'sha tilda javob ber.
Bilmagan narsangni to'qib chiqarmagin.
"""

# ===== SESSIYA =====
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = 0

# ===== YON PANEL =====
with st.sidebar:
    st.markdown("## 🇺🇿 UzbekAI")
    st.caption("Sening aqlli yordamching")

    if st.button("＋ Yangi suhbat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_id += 1
        st.rerun()

    st.divider()
    st.markdown("### ✨ Imkoniyatlar")
    st.markdown("""
    - 💬 Savollarga javob
    - 📚 Dars va matematika
    - 🌍 Ingliz tili
    - ✍️ Matn yozish
    - 💡 Yangi g'oyalar
    """)

    st.divider()
    st.caption("UzbekAI • Google Gemini")
    st.caption("API kaliti xavfsiz Secrets'da saqlanadi.")

# ===== ASOSIY SAHIFA =====
st.markdown("""
<div class="hero">
    <h1>🇺🇿 UzbekAI</h1>
    <p>Fikrlaringni yoz. Birgalikda yechim topamiz.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("#### Bugun nimada yordam beray?")
    st.caption("Quyidagi misollardan boshlashing mumkin.")

    suggestions = [
        "📚 Menga matematikani tushuntir",
        "🇬🇧 Ingliz tilidan mashq ber",
        "💡 Yangi loyiha uchun g'oya ber"
    ]

    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, use_container_width=True):
                st.session_state.pending_prompt = suggestion.split(" ", 1)[1]
                st.rerun()

# ===== SUHBAT TARIXI =====
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===== XABAR QABUL QILISH =====
prompt = st.chat_input("UzbekAI'ga xabar yoz...")

if not prompt and st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            history = []
            for message in st.session_state.messages[:-1]:
                history.append({
                    "role": (
                        "user"
                        if message["role"] == "user"
                        else "model"
                    ),
                    "parts": [{"text": message["content"]}]
                })

            chat = client.chats.create(
                model=MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
                history=history
            )

            with st.spinner("UzbekAI o'ylayapti..."):
                response = chat.send_message(prompt)

            answer = response.text or "Hozircha javob olinmadi."
            st.markdown(answer)

        except Exception as e:
            answer = (
                "Kechirasan, AI bilan bog'lanishda muammo yuz berdi. "
                "Birozdan keyin qayta urinib ko'r."
            )
            st.error(answer)
            print(f"UzbekAI xatosi: {type(e).__name__}: {e}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

st.markdown(
    '<p class="caption">UzbekAI xato qilishi mumkin. '
    'Muhim maʼlumotlarni tekshirib ko‘r.</p>',
    unsafe_allow_html=True
)
