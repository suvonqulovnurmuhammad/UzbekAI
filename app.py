
import streamlit as st
from google import genai
from google.genai import types
import time

# =====================================
# 1. SAHIFA SOZLAMALARI
# =====================================

st.set_page_config(
    page_title="UzbekAI",
    page_icon="🤖",
    layout="centered"
)

MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
Sen UzbekAI nomli bilimli, samimiy va foydali AI yordamchisan.

- Asosan ravon va tabiiy o'zbek tilida javob ber.
- Savol boshqa tilda bo'lsa, o'sha tilda javob ber.
- Faktlarni to'qib chiqarma.
- Bilmagan narsangni ochiq ayt.
- Matematikani bosqichma-bosqich tushuntir.
- Savollarga bevosita, tushunarli javob ber.
- Keraksiz takrorlardan qoch.
"""

# =====================================
# 2. DIZAYN
# =====================================

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: #f5f7ff;
}
h1 {
    text-align: center;
    color: #7c9cff;
}
.subtitle {
    text-align: center;
    color: #b8c2dc;
    margin-bottom: 25px;
}
.stChatMessage {
    border: 1px solid #293653;
    border-radius: 16px;
}
.stChatInput textarea {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 UzbekAI")
st.markdown(
    '<div class="subtitle">Sening aqlli AI yordamching</div>',
    unsafe_allow_html=True
)

# =====================================
# 3. API KALITI
# =====================================

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


api_key = get_api_key()

if not api_key:
    st.error(
        "API kaliti topilmadi. "
        "Streamlit Secrets ichida GEMINI_API_KEY "
        "sozlamasini tekshir."
    )
    st.stop()

# =====================================
# 4. SUHBAT TARIXI
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski suhbatlarni ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================
# 5. AI SO'ROVI
# =====================================

user_input = st.chat_input("UzbekAI'ga xabar yoz...")

if user_input:
    user_input = user_input.strip()

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            answer_placeholder = st.empty()

            try:
                with st.spinner("UzbekAI javob tayyorlamoqda..."):
                    client = genai.Client(
                        api_key=api_key,
                        http_options={
                            "timeout": 20000
                        }
                    )

                    # Oxirgi suhbat xabarlarini yuborish
                    history = []
                    for msg in st.session_state.messages[-12:]:
                        role = (
                            "user"
                            if msg["role"] == "user"
                            else "model"
                        )

                        history.append(
                            types.Content(
                                role=role,
                                parts=[
                                    types.Part.from_text(
                                        text=msg["content"]
                                    )
                                ]
                            )
                        )

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=history,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            max_output_tokens=700,
                            temperature=0.7
                        )
                    )

                    answer = response.text

                    if not answer or not answer.strip():
                        raise ValueError(
                            "AI bo'sh javob qaytardi."
                        )

                    answer_placeholder.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                    client.close()

            except Exception as e:
                error_text = str(e)

                answer_placeholder.error(
                    "Javob olishda xatolik yuz berdi."
                )

                st.warning(
                    "Xatolik tafsiloti: " + error_text
                )

                st.info(
                    "API kaliti, model nomi, internet "
                    "aloqasi va API limitini tekshir."
                )

                # Xato yuz berganda noto'g'ri suhbat
                # tarixini olib tashlash
                if (
                    st.session_state.messages
                    and st.session_state.messages[-1]["role"] == "user"
                ):
                    st.session_state.messages.pop()
