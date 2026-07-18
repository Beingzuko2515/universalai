import streamlit as st
import pandas as pd
from openai import OpenAI

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Universal AI Agent Dashboard", layout="wide")
st.title("🤖 Universal AI Agent Dashboard")
st.write("Your central hub for problem-solving and automated tools.")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["💬 AI Agent Chat", "📊 Data Analyst Tool", "🔍 Web Search Tool"])

# --- FETCH SECRET API KEY ---
# This looks for the hidden key securely saved on the Streamlit server
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("API Key missing! Please set up your Streamlit Secrets.")
    st.stop()

# --- PAGE 1: AI AGENT CHAT ---
if page == "💬 AI Agent Chat":
    st.header("💬 Talk to your AI Agent")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What problem can I solve for you today?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            # Real AI Call using your key
            response_placeholder = st.empty()
            completion = client.chat.completions.create(
                model="gpt-4o-mini", # Fast and highly capable model
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            ai_response = completion.choices[0].message.content
            response_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

# --- PAGE 2: DATA ANALYST TOOL ---
elif page == "📊 Data Analyst Tool":
    st.header("📊 AI Data Analyst")
    st.write("Upload a CSV file, and let the agent help you analyze it.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

# --- PAGE 3: WEB SEARCH TOOL ---
elif page == "🔍 Web Search Tool":
    st.header("🔍 Live Web Searcher")
    st.write("Search integration goes here.")