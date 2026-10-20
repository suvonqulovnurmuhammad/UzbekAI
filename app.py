
import streamlit as st
from google import genai
from datetime import datetime
from zoneinfo import ZoneInfo

# =========================
# 1. SAHIFA SOZLAMALARI
# =========================
st.set_page_config(
    page_title="Nurmuhammad's AI",
    page_icon="🇺🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 2. DIZAYN
# =========================
st.markdown("""
<style>
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
div[data-testid="stChatInput"] button {
    color: #087F72 !important;
    background: #E0FFF7 !important;
    opacity: 1 !important;
}
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
# 3. SANA VA AI SOZLAMALARI
# =========================
MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = """
Sen UzbekAI nomli aqlli va samimiy yordamchisan.

ASOSIY QOIDALAR:
- Asosan o'zbek tilida javob ber.
- Ingliz tilidagi savollarga ham javob bera ol.
- Matematika, fizika, ingliz tili va dasturlashda yordam ber.
- Kod so'ralsa, tushunarli va ishlatishga tayyor kod yoz.
- Bilmagan narsangni to'qib chiqarma.
- Javoblarni tartibli va sodda yoz.

SANA:
- Tizim bergan bugungi sana va vaqtdan foydalan.
- 2025 va 2026-yillarni avtomatik ravishda kelajak deb hisoblama.
- Sana so'ralsa, aniq sanani to'g'ridan-to'g'ri ayt.

YANGI MA'LUMOTLAR:
- Yangiliklar, sport natijalari va joriy voqealar haqida
  so'ralganda Google Search orqali qidir.
- Qidiruv natijalarini tekshir.
- Qidiruv ishlamasa yoki ma'lumot topilmasa, rostini ayt.
"""


def current_datetime():
    return datetime.now(
        ZoneInfo("Asia/Tashkent")
    ).strftime("%d-%m-%Y %H:%M:%S")


# =========================
# 4. SUHBAT MA'LUMOTLARI
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = 0

if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None


# =========================
# 5. YON PANEL
# =========================
with st.sidebar:
    st.markdown("## 🇺🇿 Nurmuhammad's AI")
    st.caption("Sening aqlli yordamching")

    if st.button("＋ Yangi suhbat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_id += 1
        st.session_state.pop("pending_prompt", None)
        st.session_state.previous_interaction_id = None
        st.rerun()

    st.divider()

    st.markdown("### ✨ Imkoniyatlar")
    st.markdown("""
    - 💬 Savollarga javob
    - 📚 Maktab fanlari
    - ➗ Matematika va fizika
    - 🇬🇧 Ingliz tili
    - ✍️ Matn va insho yozish
    - 🌐 Internetdan yangi ma'lumot qidirish
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
# 7. OLDINGI XABARLAR
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# 8. AI CHAT VA INTERNET QIDIRUVI
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
        client = None

        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")

            if not api_key:
                raise ValueError(
                    "GEMINI_API_KEY topilmadi. "
                    "Streamlit Cloud → Settings → Secrets "
                    "bo'limida API kalitini sozla."
                )

            client = genai.Client(api_key=api_key)

            now = datetime.now(ZoneInfo("Asia/Tashkent"))
            today = now.strftime("%d-%m-%Y")
            time_now = now.strftime("%H:%M:%S")

            instructions = f"""
{SYSTEM_PROMPT}

BUGUNGI SANA: {today}
HOZIRGI VAQT: {time_now}
VAQT ZONASI: Asia/Tashkent

Agar foydalanuvchi "Bugun sana nechchi?",
"Bugun qaysi kun?", "Hozir nechinchi yil?",
"Bugun qaysi oy?" yoki "Soat nechchi?" deb so'rasa,
yuqoridagi sana va vaqtga asoslanib aniq javob ber.

Joriy yangiliklar haqida so'ralsa, Google Search orqali qidir.
"""

            request_args = {
                "model": MODEL,
                "input": prompt,
                "system_instruction": instructions,
                "tools": [
                    {"type": "google_search"}
                ],
            }

            previous_id = (
                st.session_state.previous_interaction_id
            )

            if previous_id:
                request_args["previous_interaction_id"] = previous_id

            with st.spinner(
                "UzbekAI javob tayyorlamoqda..."
            ):
                response = client.interactions.create(
                    **request_args
                )

            answer = (
                getattr(response, "output_text", None) or ""
            ).strip()

            if not answer:
                answer = (
                    "Javob matni kelmadi. "
                    "Iltimos, qaytadan urinib ko'r."
                )

            st.markdown(answer)

            interaction_id = getattr(response, "id", None)

            if interaction_id:
                st.session_state.previous_interaction_id = (
                    interaction_id
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            error_text = str(e)
            error_lower = error_text.lower()

            if "429" in error_text or "quota" in error_lower:
                st.error(
                    "Gemini API kvotasi yoki so'rov limiti tugagan. "
                    "Google AI Studio'da limitni tekshir. "
                    "Kod limitni oshira olmaydi."
                )

            elif "404" in error_text or "not_found" in error_lower:
                st.error(
                    "Model topilmadi yoki ushbu API funksiyasi "
                    "loyihang uchun mavjud emas. Texnik xatoni tekshir."
                )

            elif (
                "api_key" in error_lower
                or "permission_denied" in error_lower
                or "unauthorized" in error_lower
            ):
                st.error(
                    "API kaliti noto'g'ri yoki unga ruxsat berilmagan. "
                    "Streamlit Secrets sozlamalarini tekshir."
                )

            else:
                st.error(
                    "AI bilan bog'lanishda xatolik yuz berdi."
                )

            with st.expander("Xatolik tafsilotlari"):
                st.code(f"{type(e).__name__}: {error_text}")

            # Muvaffaqiyatsiz so'rovdan keyin suhbatni davom ettirish
            st.session_state.previous_interaction_id = None

            # Xatolikdan keyin noto'g'ri javob sifatida
            # foydalanuvchi xabarini saqlab qolmaslik
            if (
                st.session_state.messages
                and st.session_state.messages[-1]["role"] == "user"
                and st.session_state.messages[-1]["content"] == prompt
            ):
                st.session_state.messages.pop()

        finally:
            if client is not None:
                try:
                    client.close()
                except Exception:
                    pass


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
