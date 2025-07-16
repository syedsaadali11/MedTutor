# streamlit_app.py
import streamlit as st
from graph import create_graph

# 📦 Initialize LangGraph
graph = create_graph()

st.set_page_config(page_title="Smart Med Tutor", layout="wide")

# 🔒 Sidebar (left panel) — Student-focused info
with st.sidebar:
    st.title("🩺 Smart Med Tutor")
    st.markdown("### 🎓 Built for Medical Students")
    st.markdown("""
**Smart Med Tutor** is your AI-powered study partner built on real medical data.  
It helps students prepare for:

- MDCAT  
- MBBS professional exams  
- Pharmacology & Pathology  
- Competitive medical entrance tests

### ✨ Features
- Understands complex medical queries  
- Instant answers from medical knowledge base   
    """)
    st.info("🎤 Voice support coming soon!")

# 📌 Main chat window (right panel)
st.title("🧠 Smart Medical Tutor")

# 📌 Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("assistant", "👋 Hello! I’m your Smart Medical Tutor. What can I assist you with today?")]
if "graph_state" not in st.session_state:
    st.session_state.graph_state = {
        "user_input": "",
        "last_question": "",
        "last_answer": "",
        "response": ""
    }

# 💬 Display chat like ChatGPT
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# 📝 Input box
if prompt := st.chat_input("Ask me any medical question..."):
    # ➕ Show user's message immediately
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append(("user", prompt))

    # 🧠 Run LangGraph with current input
    st.session_state.graph_state["user_input"] = prompt
    updated_state = graph.invoke(st.session_state.graph_state)

    # 💬 Show agent response
    response = updated_state["response"]
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append(("assistant", response))

    # 🔁 Update graph state (for follow-ups)
    st.session_state.graph_state.update(updated_state)
