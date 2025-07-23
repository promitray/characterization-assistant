from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def build_vector_store(text: str, api_key: str, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = splitter.split_text(text)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    return FAISS.from_texts(chunks, embeddings)

def retrieve_context(vector_store, query: str, k=3) -> str:
    if not vector_store:
        return ""
    docs = vector_store.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])
