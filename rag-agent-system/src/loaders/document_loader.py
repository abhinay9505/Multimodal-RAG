from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

def load_document(file_path, file_type):
    if file_type == "application/pdf":
        return PyPDFLoader(file_path).load()
    else:
        return Docx2txtLoader(file_path).load()