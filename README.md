# 🤖 GovTech Developer Assistant

A web-based **RAG-powered chatbot** that allows users to interact with publicly available information about Singapore GovTech products and APIs. Built with **Streamlit**, **LangChain**, **OpenAI**, and **ChromaDB**.

---

## Features

- Conversational interface to ask questions about GovTech products
- Retrieval-Augmented Generation (RAG) using vector embeddings
- Collapsible chat history
- Sample prompts for users
- Simple login/password protection

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/fernandatan/govtechapp-aichampions.git
cd govtechapp-aichampions
```

2. **Create a virtual environment and activate it:**
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
OPENAI_API_KEY=your_openai_api_key
APP_USERNAME=admin
APP_PASSWORD=password123
```

---

## Start the application
```bash
python3 run_backend.py
```

1. Log in using the credentials from your .env.
2. Type a question or click a sample prompt.
3. Chat with the assistant about GovTech products and APIs.


