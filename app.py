
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="UzbekAI",
    page_icon="🇺🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 1. DIZAYN
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
section[data-testid="stSidebar"] h3 {
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
    background: linear-gradient(90deg, #38F9D7, #60A5FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #C4D2E8 !important;
    font-size: 1.08rem;
}
.stApp p, .stApp li, .stApp label,
.stApp h2, .stApp h3,
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
    .hero h1 { font-size: 2.2rem !important; }
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# 2. AI SOZLAMALARI
# =========================
MODEL = "gemini-3.5-flash-lite"


SYSTEM_PROMPT = """
Sen UzbekAI nomli bilimli, samimiy va puxta yordamchisan.

TIL VA IMLO:
- Asosan tabiiy, ravon va adabiy o'zbek tilida javob ber.
- O'zbekcha so'zlarni to'g'ri yoz, grammatik xatolarni kamaytir.
- Fikrlarni aniq, tartibli va tushunarli ifoda et.
- Foydalanuvchi boshqa tilda so'rasa, o'sha tilda javob ber.

ANIQLIK:
- Faktlarni to'qib chiqarma.
- Hozirgi sana, futbolchi klubi, transfer, o'yin hisobi,
  yangilik, narx yoki joriy ma'lumot so'ralsa, internetdan tekshir.
- Eski ma'lumotga tayanib hozirgi holatni taxmin qilma.
- Ishonchli ma'lumot topilmasa, buni ochiq ayt.
- Qarama-qarshi manbalar bo'lsa, noaniqlikni tushuntir.
- Imkon qadar ishonchli manbalarga tayan.

JAVOB SIFATI:
- Savolga bevosita javob ber, keyin kerakli izohlarni qo'sh.
- Murakkab mavzularni bosqichma-bosqich tushuntir.
- Matematika va fizika masalalarida yechimni tekshir.
- Keraksiz takrorlardan qoch.
"""

# =========================
# 3. CHAT TARIXINI BOSHQARISH
# =========================
if "chats" not in st.session_state:
    old_messages = st.session_state.get("messages", [])

    st.session_state.chats = {
        "1": {
            "title": "Eski suhbat" if old_messages else "Yangi suhbat",
            "messages": list(old_messages)
        }
    }
    st.session_state.active_chat_id = "1"
    st.session_state.chat_counter = 1

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = "1"

if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = len(st.session_state.chats)

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# =========================
# 4. YON PANEL
# =========================
with st.sidebar:
    st.markdown("## 🇺🇿 UzbekAI")
    st.caption("Sening aqlli yordamching")

    if st.button("＋ Yangi suhbat", use_container_width=True):
        st.session_state.chat_counter += 1
        new_id = str(st.session_state.chat_counter)

        st.session_state.chats[new_id] = {
            "title": "Yangi suhbat",
            "messages": []
        }

        st.session_state.active_chat_id = new_id
        st.session_state.pending_prompt = None
        st.rerun()

    st.divider()
    st.markdown("### 💬 Suhbatlar")

    # Eng yangi suhbatlar birinchi ko'rinadi
    for cid in reversed(list(st.session_state.chats.keys())):
        chat_title = st.session_state.chats[cid]["title"]
        is_active = cid == st.session_state.active_chat_id

        label = ("📍 " if is_active else "💬 ") + chat_title[:32]

        if st.button(
            label,
            key=f"open_chat_{cid}",
            use_container_width=True
        ):
            st.session_state.active_chat_id = cid
            st.session_state.pending_prompt = None
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
    st.caption("Model: Google Gemini")
    st.caption("UzbekAI • 2026")

# Faol suhbatni tanlaymiz
active_chat = st.session_state.chats[
    st.session_state.active_chat_id
]
messages = active_chat["messages"]

# =========================
# 5. ASOSIY SAHIFA
# =========================
st.markdown("""
<div class="hero">
    <h1>🇺🇿 UzbekAI</h1>
    <p>Fikrlaringni yoz. Birgalikda yechim topamiz.</p>
</div>
""", unsafe_allow_html=True)

if not messages:
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
# 6. FAOL CHAT XABARLARI
# =========================
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 7. YANGI XABAR VA AI JAVOBI
# =========================
prompt = st.chat_input("UzbekAI'ga xabar yoz...")

if not prompt and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            # Suhbat tarixini AI ga yuborish
            conversation = SYSTEM_PROMPT + "\n\nSuhbat tarixi:\n"

            for message in messages[:-1]:
                role = (
                    "Foydalanuvchi"
                    if message["role"] == "user"
                    else "UzbekAI"
                )
                conversation += (
                    f"\n{role}: {message['content']}\n"
                )

            conversation += (
                f"\nFoydalanuvchining yangi savoli: {prompt}\n"
                "Zamonaviy yoki o'zgaruvchan faktlar bo'lsa, "
                "Google Search orqali tekshir. "
                "Javobni o'zbek tilida ravon va aniq yoz."
            )

            with st.spinner("UzbekAI ma'lumotlarni tekshiryapti..."):
                result = client.interactions.create(
                    model=MODEL,
                    input=conversation,
                    tools=[{"type": "google_search"}]
                )

            answer = result.output_text or "Javob olinmadi."
            st.markdown(answer)

            # Topilgan manbalarni ko'rsatish
            source_links = []
            for step in (result.steps or []):
                if getattr(step, "type", "") != "model_output":
                    continue

                for block in (getattr(step, "content", []) or []):
                    for citation in (
                        getattr(block, "annotations", []) or []
                    ):
                        if getattr(citation, "type", "") == "url_citation":
                            url = getattr(citation, "url", None)
                            title = getattr(citation, "title", None) or "Manba"

                            if url and url not in [
                                item[1] for item in source_links
                            ]:
                                source_links.append((title, url))

            if source_links:
                with st.expander("🔎 Foydalanilgan manbalar"):
                    for title, url in source_links:
                        st.markdown(f"- [{title}]({url})")


        except Exception as e:
            answer = (
                "Kechirasan, AI bilan bog'lanishda xatolik yuz berdi. "
                "Birozdan keyin qayta urinib ko'r."
            )
            st.error(answer)
            print(f"UzbekAI xatosi: {type(e).__name__}: {e}")

    messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# =========================
# 8. PASTKI ESLATMA
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
