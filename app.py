import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate

# ---------------- LOAD ENV ----------------
load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("hf")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Chatbot Mentor", page_icon="🤖")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "module" not in st.session_state:
    st.session_state["module"] = None

if "chat" not in st.session_state:
    st.session_state["chat"] = []

# ---------------- MODULES ----------------
MODULES = [
    "Python",
    "SQL",
    "Power BI",
    "EDA",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Agentic AI"
]

REJECTION_MSG = (
    "Sorry, I don’t know about this question. "
    "Please ask something related to the selected module."
)

# ===================== HOME PAGE =====================
if st.session_state["page"] == "home":

    st.title("👋 Welcome to AI Chatbot Mentor")
    st.subheader("Your personalized AI learning assistant")
    st.write("Please select a learning module to begin your mentoring session.")

    selected_module = st.selectbox("📌 Select a Module",["Please select Module"] + MODULES)

    if selected_module == "Please select Module":
        selected_module = ""

    if selected_module and st.button("Start Mentoring"):
        st.session_state.module = selected_module
        st.session_state.page = "chat"
        st.session_state.chat = []
        st.rerun()

# ===================== CHAT PAGE =====================
if st.session_state.page == "chat":

    st.title(f"🎯 {st.session_state.module} AI Mentor")
    st.write(f"I am your dedicated mentor for **{st.session_state.module}**.")
    st.write("How can I help you today?")

    # ---------------- LLM ----------------
    base_llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-V3.2",
        task="conversational",
        temperature=0.7,
        max_new_tokens=512,
        streaming=True   # 👈 IMPORTANT
    )

    llm = ChatHuggingFace(llm=base_llm)

    # ---------------- PROMPT ----------------
    prompt_template = PromptTemplate(
        input_variables=["question"],
        template=f"""
You are a mentor ONLY for {st.session_state.module}.
Answer questions related ONLY to {st.session_state.module}.
If the question is outside this domain, reply exactly with:
"{REJECTION_MSG}"

Question: {{question}}
"""
    )

    # ---------------- SHOW CHAT HISTORY ----------------
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------- CHAT INPUT ----------------
    user_input = st.chat_input("Ask your question...")

    if user_input:
        # store user message
        st.session_state.chat.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        formatted_prompt = prompt_template.format(question=user_input)

        # ---------------- STREAM RESPONSE ----------------
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_placeholder = st.empty()
                final_response = ""
                
                response = llm.stream(formatted_prompt)
                for chunk in response:
                    if chunk.content:
                        final_response += chunk.content
                        response_placeholder.markdown(final_response)

        st.session_state.chat.append(
            {"role": "assistant", "content": final_response}
        )

    # ---------------- DOWNLOAD CHAT ----------------
    if st.session_state.chat:
        chat_text = ""
        for msg in st.session_state.chat:
            role = "User" if msg["role"] == "user" else "AI"
            chat_text += f"{role}: {msg['content']}\n\n"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name=f"AI_Chatbot_Mentor_{timestamp}.txt",
            mime="text/plain"
        )

    # ---------------- BACK BUTTON ----------------
    if st.button("⬅ Back to Modules"):
        st.session_state.page = "home"
        st.session_state.chat = []
        st.rerun()
