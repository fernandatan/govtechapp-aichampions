from langchain_community.document_loaders import PlaywrightURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import json
from dotenv import load_dotenv
import os

load_dotenv()

PRODUCT_URLS_PATH = os.path.join("data", "product_urls.json")

# Load URLs
with open(PRODUCT_URLS_PATH, "r") as f:
    urls = json.load(f)

print(f"Loaded {len(urls)} product URLs...")

# Use Playwright loader (renders JavaScript!)
loader = PlaywrightURLLoader(
    urls=urls,
    remove_selectors=["header", "footer", "nav", "script", "style"]
)

docs = loader.load()
print(f"Fetched {len(docs)} documents.")

# Split content into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
split_docs = splitter.split_documents(docs)
print(f"Split into {len(split_docs)} chunks.")

# Store in ChromaDB
vectorstore = Chroma.from_documents(
    split_docs,
    embedding=OpenAIEmbeddings(),  
    persist_directory="./govtech_chroma"
)

vectorstore.persist()
print("✅ Documents successfully embedded and stored.")

# from langchain_community.document_loaders import AsyncHtmlLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
# import json
# from dotenv import load_dotenv
# import os

# load_dotenv()
# openai_key = os.getenv("OPENAI_API_KEY")

# PRODUCT_URLS_PATH = os.path.join("data", "product_urls.json")

# # Load URLs
# with open(PRODUCT_URLS_PATH, "r") as f:
#     urls = json.load(f)

# # Load HTML content
# loader = AsyncHtmlLoader(urls)
# docs = loader.load()

# # Split content
# splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
# split_docs = splitter.split_documents(docs)

# # Store in ChromaDB
# vectorstore = Chroma.from_documents(
#     split_docs,
#     embedding=OpenAIEmbeddings(),  # Ensure your OpenAI key is set
#     persist_directory="./govtech_chroma"
# )

# vectorstore.persist()
# print("Documents successfully embedded and stored.")
