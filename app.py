
import streamlit as st
from google import genai
from google.genai import types

# =========================
# 1. SAHIFA SOZLAMALARI
# =========================
st.set_page_config(
    page_title="Nurmuhammad's AI",
    page_icon="uz",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 2. ZAMONAVIY DIZAYN
# =========================
st.markdown("""
<style>
/* Asosiy sahifa */
.stApp {
    background: #0B1020 !important;
    color: #F8FAFC !important;
}

header[data-testid="stHeader"] {
    background: #0B1020 !important;
}

.block-container {
    max-width: 950px;
    padding-top: 1.8rem;
    padding-bottom: 7rem;
}

/* Yon panel */
section[data-testid="stSidebar"] {
    background: #151D32 !important;
    border-right: 2px solid #334568 !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] li {
    color: #F8FAFC !important;
}

/* Yon panel tugmalari */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"] {
    background: #263653 !important;
    color: #FFFFFF !important;
    opacity: 1 !important;
}

[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg,
button[kind="header"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* UzbekAI sarlavhasi */
.hero {
    text-align: center;
    padding: 26px 10px 22px;
}

.hero h1 {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #38F9D7, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #C4D2E8 !important;
    font-size: 1.08rem;
}

/* Asosiy matnlar */
.stApp p,
.stApp li,
.stApp label,
.stApp h2,
.stApp h3,
.stApp [data-testid="stMarkdownContainer"] {
    color: #F1F5F9;
}

.stApp [data-testid="stCaptionContainer"],
.stApp small {
    color: #C0CDE0 !important;
}

/* Suhbat xabarlari */
div[data-testid="stChatMessage"] {
    background: #182238 !important;
    border: 1px solid #354765 !important;
    border-radius: 18px !important;
    padding: 16px !important;
    margin-bottom: 14px !important;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] strong {
    color: #F8FAFC !important;
}

/* Xabar yozish maydoni */
div[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 2px solid #38DCC0 !important;
    border-radius: 17px !important;
}

div[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #0891B2 !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
    opacity: 1 !important;
}

/* Xabar yuborish tugmasi */
div[data-testid="stChatInput"] button {
    color: #087F72 !important;
    background: #E0FFF7 !important;
    opacity: 1 !important;
}

/* Boshqa tugmalar */
.stButton > button {
    background: #203454 !important;
    color: #FFFFFF !important;
    border: 1px solid #5B83B8 !important;
    border-radius: 13px !important;
    font-weight: 600 !important;
    min-height: 43px;
}

.stButton > button p,
.stButton > button span {
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background: #0E766E !important;
    border-color: #4FFFE0 !important;
}

/* Kichik ekranlarga moslashish */
@media (max-width: 640px) {
    .hero h1 {
        font-size: 2.2rem !important;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# 3. AI SOZLAMALARI
# =========================
MODEL = "gemini-2.5-flash-lite"

SYSTEM_PROMPT = """
Sen UzbekAI nomli aqlli va samimiy yordamchisan.
Asosan o'zbek tilida, sodda va tushunarli javob ber.
Ingliz tilida savol berilsa, kerak bo'lsa ingliz tilida javob ber.
Matematika, fizika, ingliz tili, dasturlash va boshqa fanlarda
bosqichma-bosqich yordam ber.
Javoblarni tartibli va o'qishga qulay yoz.
Bilmagan narsangni to'qib chiqarmagin.
"""

# =========================
# 4. SUHBAT MA'LUMOTLARI
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = 0

# =========================
# 5. YON PANEL
# =========================
with st.sidebar:
    st.markdown(" Nurmuhammad's AI")
    st.caption("Sening aqlli yordamching")

    if st.button("＋ Yangi suhbat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_id += 1
        st.session_state.pop("pending_prompt", None)
        st.rerun()

    st.divider()

    st.markdown("### ✨ Imkoniyatlar")
    st.markdown("""
    - 💬 Savollarga javob
    - 📚 Maktab fanlari
    - ➗ Matematika va fizika
    - 🇬🇧 Ingliz tili
    - ✍️ Matn va insho yozish
    - 💡 Yangi g'oyalar
    """)

    st.divider()
    st.caption("Powered by Suvonqulov Nurmuhammad")
    st.caption("UzbekAI • 2026")

# =========================
# 6. ASOSIY SAHIFA
# =========================
st.markdown("""
<div class="hero">
    <h1>🇺🇿 Nurmuhammad's AI</h1>
    <p>Fikrlaringni yoz. Birgalikda yechim topamiz.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("### Bugun nimada yordam beray?")
    st.caption("Boshlash uchun quyidagi mavzulardan birini tanla.")

    col1, col2, col3 = st.columns(3)

    if col1.button("📚 Maktab fanlari", use_container_width=True):
        st.session_state.pending_prompt = (
            "Menga maktab fanlaridan yordam ber."
        )
        st.rerun()

    if col2.button("🇬🇧 Ingliz tili", use_container_width=True):
        st.session_state.pending_prompt = (
            "Men bilan ingliz tili mashqini boshlagin."
        )
        st.rerun()

    if col3.button("💡 Yangi g'oyalar", use_container_width=True):
        st.session_state.pending_prompt = (
            "Menga foydali va qiziqarli loyiha g'oyalarini ber."
        )
        st.rerun()

# =========================
# 7. OLDINGI XABARLARNI KO'RSATISH
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 8. FOYDALANUVCHI XABARI
# =========================
prompt = st.chat_input("UzbekAI'ga xabar yoz...")

if not prompt and st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

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

            answer = response.text or "Javob olinmadi."
            st.markdown(answer)

        except Exception as e:
            answer = (
                "Kechirasan, AI bilan bog'lanishda xatolik yuz berdi. "
                "Birozdan keyin qayta urinib ko'r."
            )
            st.error(answer)
            print(f"UzbekAI xatosi: {type(e).__name__}: {e}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

# =========================
# 9. PASTKI ESLATMA
# =========================
st.markdown("""
<div style="
    text-align:center;
    color:#C0CDE0;
    font-size:0.82rem;
    padding:20px 0 5px;
">
    UzbekAI • Sun'iy intellekt yordamchisi
    <br>
    Muhim ma'lumotlarni tekshirib ko'r.
</div>
""", unsafe_allow_html=True)
