import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# -------------------
# CONFIGURE LOGIN DETAILS
# -------------------
VALID_USERNAME = os.getenv("APP_USERNAME", "admin")
VALID_PASSWORD = os.getenv("APP_PASSWORD", "password123") 

st.set_page_config(page_title="GovTech Developer Assistant", page_icon="🤖")

# -------------------
# SESSION STATE INIT
# -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = Chroma(
        persist_directory=None,
        embedding_function=OpenAIEmbeddings()
    )

if "retriever" not in st.session_state:
    st.session_state.retriever = st.session_state.vectorstore.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 4}
    )

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True,
        output_key="answer"
    )

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None 

# -------------------
# LOGIN FUNCTION
# -------------------
def login(username, password):
    """Check username and password."""
    return username == VALID_USERNAME and password == VALID_PASSWORD


# -------------------
# LOGIN PAGE
# -------------------
def show_login():
    st.title("🔐 Login")
    st.markdown("Please enter your username and password to continue.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")


# -------------------
# MAIN CHATBOT PAGE
# -------------------
def show_chatbot():
    st.set_page_config(page_title="GovTech Dev Assistant")

    st.title("🤖 GovTech Developer Assistant")
    st.caption("Ask anything about GovTech products and APIs.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    # if "pending_prompt" not in st.session_state:
    #     st.session_state.pending_prompt = None

        # Handle sample prompt clicks BEFORE rendering the text_input
    st.markdown("💡 **Try one of these sample prompts:**")
    cols = st.columns(2)
    with cols[0]:
        if st.button("What is Government on Commercial Cloud?"):
            st.session_state.input_text = "What is Government on Commercial Cloud?"
            st.rerun()
    with cols[1]:
        if st.button("Explain how teams can use Cloak"):
            st.session_state.input_text = "Explain how teams can use Cloak"
            st.rerun()

    # Pre-fill input if a sample was chosen
    # default_text = st.session_state.pending_prompt or ""
    user_input = st.text_input("Ask a question:", key="input_text", placeholder="Type your question here...")

    # Reset pending prompt after use
    # st.session_state.pending_prompt = None

    # Load vector store
    vectorstore = Chroma(persist_directory="./govtech_chroma", embedding_function=OpenAIEmbeddings())

    # Set up LangChain
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0, model="gpt-4"),
        retriever=retriever,
        memory=memory
    )

    # --- Run chatbot ---
    if user_input and st.session_state.get("last_input") != user_input:
        with st.spinner("Generating response..."):
            response = qa_chain.run(user_input)
            st.session_state.chat_history.append((user_input, response))
            st.session_state.last_input = user_input  # prevent repeat on rerun

    # Display current answer and collapsible history
    if st.session_state.chat_history:
        latest_question, latest_answer = st.session_state.chat_history[-1]
        st.markdown(f"**🧑 You:** {latest_question}")
        st.markdown(f"**🤖 Assistant:** {latest_answer}")

        with st.expander("🕘 Show past chat history"):
            for q, a in reversed(st.session_state.chat_history[:-1]):
                st.markdown(f"**You:** {q}")
                st.markdown(f"**Assistant:** {a}")
                st.markdown("---")


# -------------------
# APP ENTRY POINT
# -------------------
if not st.session_state.logged_in:
    show_login()
else:
    show_chatbot()