# 💬 Multi-Chat AI Chatbot

A fully functional **Chatbot** built with **Streamlit**, **LangChain**, and **OpenAI's GPT models**.  
Features include **multi-chat sessions**, per-chat **domain context**, **auto-naming from first message**, and a modern conversational interface.

---

## 🚀 Features

- ChatGPT-like UI using `st.chat_message` & `st.chat_input`
- Multiple chat sessions stored in the sidebar
- Auto-naming chats from first user message
- Domain-specific context stored for each chat
- Domain picker that updates automatically when switching chats
- Temperature control for creativity level
- Uses user-supplied OpenAI API key — no need to embed your own key
- LangChain integration for prompt templating and conversation memory handling

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** – UI framework
- **LangChain** – Conversation & prompt management
- **OpenAI API** – LLM models (GPT-4, GPT-3.5, etc.)
- **python-dotenv** – Environment variable management

---

## 📂 Project Structure

├── app.py # Main Streamlit app with UI and chat session logic
├── utils.py # LangChain prompt template and LLM response function
├── requirements.txt
├── .env.example # Example environment file for secrets
└── README.md


---

## ⚙️ Setup & Installation

1. **Clone this repository**
    ```
    git clone https://github.com/yourusername/chatgpt-style-chatbot.git
    cd chatgpt-style-chatbot
    ```

2. **Create a virtual environment**
    ```
    python -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate      # Windows
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Configure environment variables**

    - Create a `.env` file:
        ```
        LANGCHAIN_API_KEY=your_langchain_api_key
        ```
    - *(OpenAI API key is entered by each user in the app’s sidebar)*

---

## ▶️ Usage (Local)

Run the app locally:

streamlit run app.py

- Enter your **OpenAI API key** in the sidebar
- Select a **domain** for your chat or create a new one
- Start chatting! Create multiple chats from the sidebar and switch between them

---

## 📜 License

This project is licensed under the MIT License.