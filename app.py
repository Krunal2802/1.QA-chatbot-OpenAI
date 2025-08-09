import streamlit as st
from utils import generate_response
import os
from dotenv import load_dotenv

# ---------- Load environment variables ----------
load_dotenv()

# LangSmith tracking (optional)
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q/A chatbot with OpenAI"

st.set_page_config(page_title="Q/A Chatbot", page_icon="💬", layout="wide")
st.title("💬 Q/A Chatbot with OpenAI")

# ---------- Available domains ----------
available_domains = [
    "App Development",
    "Web Development",
    "ML Engineering",
    "Generative AI Engineering"
]

# ---------- Sidebar: API key & settings ----------
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
llm = st.sidebar.selectbox(
    "Select an OpenAI model:",
    ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
)

# Initialize selector state
if "domain_selector" not in st.session_state:
    st.session_state["domain_selector"] = available_domains[0]

temperature = st.sidebar.slider(
    "Temperature (creativity):", 0.0, 1.0, 0.7, step=0.1,
    help="Lower = more precise and deterministic. Higher = more creative and varied."
)

# Fixed internally
max_tokens = 1000

# ---------- Session State Init ----------
if "sessions" not in st.session_state:
    st.session_state["sessions"] = {}  # {chat_id: {"title": str, "domain": str, "messages": []}}
if "current_chat" not in st.session_state:
    st.session_state["current_chat"] = None

# ---------- Sidebar: Chat List ----------
st.sidebar.markdown("### 💾 Your Chats")

# New Chat Button
if st.sidebar.button("➕ New Chat"):
    chat_id = f"chat_{len(st.session_state['sessions']) + 1}"
    st.session_state["sessions"][chat_id] = {
        "title": "New Chat",
        "domain": st.session_state["domain_selector"],  # store current selector value
        "messages": []
    }
    st.session_state["current_chat"] = chat_id
    st.rerun()

if st.session_state["sessions"]:
    # Labels only show title
    chat_labels = [cdata['title'] for cdata in st.session_state["sessions"].values()]
    chat_ids = list(st.session_state["sessions"].keys())

    selected_label = st.sidebar.radio(
        "Select a chat:",
        chat_labels,
        index=(chat_ids.index(st.session_state["current_chat"])
               if st.session_state["current_chat"] in chat_ids else 0)
    )

    # Map label back to chat_id
    selected_chat_id = chat_ids[chat_labels.index(selected_label)]
    if selected_chat_id != st.session_state["current_chat"]:
        st.session_state["current_chat"] = selected_chat_id
        # Sync domain selector to that chat's stored domain
        st.session_state["domain_selector"] = st.session_state["sessions"][selected_chat_id]["domain"]
        st.rerun()

    # Show domain selector (editable, updates current chat's domain)
    selected_domain = st.sidebar.selectbox(
        "Domain for current chat:",
        available_domains,
        key="domain_selector"
    )
    # Update stored domain if changed
    if st.session_state["sessions"][st.session_state["current_chat"]]["domain"] != selected_domain:
        st.session_state["sessions"][st.session_state["current_chat"]]["domain"] = selected_domain
else:
    st.sidebar.info("No chats yet. Click '➕ New Chat' to start!")

# ---------- Main Chat Area ----------
if st.session_state["current_chat"] is None:
    st.info("👈 Start a new chat from the left sidebar!")
else:
    chat_id = st.session_state["current_chat"]
    chat_data = st.session_state["sessions"][chat_id]
    messages = chat_data["messages"]

    # Styled domain tag
    st.markdown(
        f"<div style='padding:6px 12px; background-color:#eef6ff; border-radius:8px; "
        f"margin-bottom:10px; font-size:14px;'>🏷 <b>Domain:</b> {chat_data['domain']}</div>",
        unsafe_allow_html=True
    )

    # Render history
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # If first message, rename chat
        if len(messages) == 0:
            pretty_title = prompt.strip()
            if len(pretty_title) > 30:
                pretty_title = pretty_title[:30] + "..."
            chat_data["title"] = pretty_title

        # Add user message
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant reply
        response = generate_response(
            messages, api_key, llm, temperature, max_tokens, chat_data["domain"]
        )

        # Append assistant message
        messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)