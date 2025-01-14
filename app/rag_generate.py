from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from scipy.stats import fisher_exact

def initialize_faiss():
    # Folder tempat file teks
    folder_path = "data/health_tips"

    documents = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            loader = TextLoader(os.path.join(folder_path, file_name))
            documents.extend(loader.load())

    # Membagi dokumen menjadi bagian kecil
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Menggunakan SentenceTransformer untuk embedding
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
    vectorstore = FAISS.from_documents(texts, embeddings)

    # Menyimpan indeks
    vectorstore.save_local("data/faiss_index")
    print("FAISS index berhasil dibuat.")

# Jalankan fungsi inisialisasi
if __name__ == "__main__":
    initialize_faiss()
