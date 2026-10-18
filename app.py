
import streamlit as st

st.set_page_config(
    page_title="UzbekAI",
    page_icon="🤖"
)

st.title("🇺🇿 UzbekAI")
st.subheader("Sening aqlli yordamching!")

st.write(
    "Salom! Men UzbekAI. "
    "Tez orada sen bilan suhbatlashishni boshlayman."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Salom! Men UzbekAI. Senga qanday yordam bera olaman?"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("UzbekAI'ga xabar yoz...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    answer = (
        "Xabaringni oldim! Hozircha men sinov rejimidaman. "
        "Keyingi bosqichda haqiqiy AI modelini ulaymiz."
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)
