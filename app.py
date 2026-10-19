
import streamlit as st
from google import genai

# =====================================
# 1. SAHIFA SOZLAMALARI
# =====================================
st.set_page_config(
    page_title="UzbekAI",
    page_icon="🇺🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# 2. DIZAYN
# =====================================
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
    padding-top: 1.5rem;
    padding-bottom: 6rem;
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
.hero {
    text-align: center;
    padding: 20px 10px;
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
.stApp h2, .stApp h3 {
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
    margin-bottom: 12px !important;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li {
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
}
.stButton > button {
    background: #203454 !important;
    color: #FFFFFF !important;
    border: 1px solid #5B83B8 !important;
    border-radius: 12px !important;
    min-height: 42px;
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

# =====================================
# 3. AI KO'RSATMALARI
# =====================================
MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = """
Sen UzbekAI nomli bilimli, samimiy va foydali AI yordamchisan.

O'ZBEK TILI:
- Asosan adabiy, tabiiy va ravon o'zbek tilida javob ber.
- Imlo va grammatikaga e'tibor ber.
- O'zbekcha apostroflarni va so'zlarni to'g'ri yoz.
- Savol boshqa tilda berilsa, o'sha tilda javob ber.

ANIQLIK:
- Faktlarni to'qib chiqarma.
- Bilmagan narsangni bilaman deb aytma.
- Hozirgi yangiliklar, futbolchilar klubi, transferlar,
  o'yin natijalari va joriy ma'lumotlarni Google Search
  orqali tekshir.
- Ma'lumotning sanasiga e'tibor ber.
- Ishonchli manba topilmasa, buni ochiq ayt.
- Eski ma'lumotni hozirgi fakt sifatida ko'rsatma.
- Taxminni aniq fakt bilan aralashtirma.

JAVOB SIFATI:
- Savolga bevosita javob ber.
- Kerakli joyda batafsil tushuntir va misollar keltir.
- Matematika va fizika masalalarini bosqichma-bosqich yech.
- Ingliz tilini sodda va tushunarli o'rgat.
- Foydalanuvchining savolini diqqat bilan tushun.
- Keraksiz takrorlardan qoch.
"""

# =====================================
# 4. CHAT XOTIRASI
# =====================================
if "chats" not in st.session_state:
    st.session_state.chats = {
        "1": {
            "title": "Yangi suhbat",
            "messages": []
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

# =====================================
# 5. YON PANEL VA CHAT RO'YXATI
# =====================================
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

    for cid in reversed(list(st.session_state.chats.keys())):
        title = st.session_state.chats[cid]["title"]
        marker = "📍 " if cid == st.session_state.active_chat_id else "💬 "

        if st.button(
            marker + title[:30],
            key=f"chat_{cid}",
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
    - ✍️ Insho va matnlar
    - ⚽ Futbol va yangiliklar
    """)

    st.divider()
    st.caption("Google Gemini + Search")
    st.caption("UzbekAI • 2026")

active_chat = st.session_state.chats[
    st.session_state.active_chat_id
]
messages = active_chat["messages"]

# =====================================
# 6. ASOSIY SAHIFA
# =====================================
st.markdown("""
<div class="hero">
    <h1>🇺🇿 UzbekAI</h1>
    <p>Fikrlaringni yoz. Birgalikda yechim topamiz.</p>
</div>
""", unsafe_allow_html=True)

if not messages:
    st.markdown("### Bugun nimada yordam beray?")
    st.caption("Quyidagi mavzulardan birini tanlashing mumkin.")

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

    if col3.button("⚽ Futbol yangiliklari", use_container_width=True):
        st.session_state.pending_prompt = (
            "Futbolga oid eng yangi yangiliklarni ishonchli "
            "internet manbalaridan tekshirib tushuntir."
        )
        st.rerun()

# =====================================
# 7. OLDINGI XABARLAR
# =====================================
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================
# 8. FOYDALANUVCHI SAVOLI
# =====================================
prompt = st.chat_input("UzbekAI'ga xabar yoz...")

if not prompt and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    if not any(m["role"] == "user" for m in messages):
        title = prompt.strip().replace("\n", " ")
        active_chat["title"] = (
            title[:30] + "..." if len(title) > 30 else title
        )

    messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            # Oldingi suhbatni modelga kontekst sifatida berish
            conversation = []

            for msg in messages[:-1]:
                role = (
                    "Foydalanuvchi"
                    if msg["role"] == "user"
                    else "UzbekAI"
                )
                conversation.append(
                    f"{role}: {msg['content']}"
                )

            conversation.append(
                f"Foydalanuvchining yangi savoli: {prompt}"
            )

            full_input = "\n\n".join(conversation)

            with st.spinner(
                "UzbekAI javob tayyorlayapti va ma'lumotni tekshiryapti..."
            ):
                response = client.interactions.create(
                    model=MODEL,
                    input=full_input,
                    system_instruction=SYSTEM_PROMPT,
                    tools=[{"type": "google_search"}]
                )

            answer = (
                getattr(response, "output_text", None)
                or "Javob olinmadi. Savolni qayta yuborib ko'r."
            )

            # Google Search qaytargan manbalarni topish
            sources = []
            for step in (getattr(response, "steps", None) or []):
                if getattr(step, "type", "") != "model_output":
                    continue

                for block in (
                    getattr(step, "content", None) or []
                ):
                    for citation in (
                        getattr(block, "annotations", None) or []
                    ):
                        if getattr(citation, "type", "") == "url_citation":
                            url = getattr(citation, "url", None)
                            name = (
                                getattr(citation, "title", None)
                                or "Manba"
                            )

                            if url and all(
                                existing_url != url
                                for _, existing_url in sources
                            ):
                                sources.append((name, url))

            # Manbalarni javobga qo'shish:
            # ular chat qayta ochilganda ham saqlanadi
            if sources:
                answer += "\n\n**🔎 Foydalanilgan manbalar:**\n"
                for name, url in sources:
                    answer += f"\n- [{name}]({url})"

            st.markdown(answer)

        except Exception as e:
            print(f"UzbekAI xatosi: {type(e).__name__}: {e}")
            answer = (
                "Kechirasan, hozir javob olishda xatolik yuz berdi. "
                "Internet aloqasini, API kalitini va model sozlamalarini "
                "tekshirib, yana urinib ko'r."
            )
            st.error(answer)

    messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# =====================================
# 9. PASTKI ESLATMA
# =====================================
st.markdown("""
<div style="
    text-align:center;
    color:#C0CDE0;
    font-size:0.82rem;
    padding:20px 0 5px;
">
    UzbekAI • Sun'iy intellekt yordamchisi
    <br>
    Muhim ma'lumotlarni ishonchli manbalardan tekshir.
</div>
""", unsafe_allow_html=True)
