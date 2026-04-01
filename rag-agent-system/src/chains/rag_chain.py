from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def build_rag_chain(retriever, model, format_docs):

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer based only on context"),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}")
    ])

    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()
    )