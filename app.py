
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
    background: #101218;
    color: #ECECF1;
}
header[data-testid="stHeader"] {
    background: rgba(16,18,24,0.9);
}
section[data-testid="stSidebar"] {
    background: #171A22;
    border-right: 1px solid #292D38;
}
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}
.hero {
    text-align: center;
    padding: 30px 12px 24px;
}
.hero h1 {
    font-size: 2.7rem;
    font-weight: 750;
    letter-spacing: -1.5px;
    background: linear-gradient(90deg, #68E0CF, #8AA8FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #A7ADBD;
    font-size: 1.05rem;
}
div[data-testid="stChatMessage"] {
    border: 1px solid #292D38;
    border-radius: 18px;
    padding: 16px;
    background: #171A22;
    margin-bottom: 14px;
}
div[data-testid="stChatInput"] {
    border-radius: 18px;
}
.stButton > button {
    border-radius: 12px;
    border: 1px solid #343A49;
    background: #202530;
    color: #F4F5F8;
    min-height: 42px;
}
.stButton > button:hover {
    border-color: #68E0CF;
    color: #68E0CF;
}
.caption {
    color: #8991A3;
    font-size: 0.82rem;
    text-align: center;
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
