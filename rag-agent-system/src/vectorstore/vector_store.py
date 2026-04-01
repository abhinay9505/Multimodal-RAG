from langchain_community.vectorstores import FAISS

def create_vectorstore(chunks, embeddings):
    return FAISS.from_documents(chunks, embeddings)

def get_retriever(db):
    return db.as_retriever()