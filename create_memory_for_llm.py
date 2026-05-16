# from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings

# from langchain_community.vectorstores import FAISS

# ## Uncomment the following files if you're not using pipenv as your virtual environment manager
# # from dotenv import load_dotenv
# # load_dotenv()


# # Step 1: Load raw PDF(s)
# DATA_PATH="data/"
# def load_pdf_files(data):
#     loader = DirectoryLoader(data,
#                              glob='*.pdf',
#                              loader_cls=PyPDFLoader)
    
#     documents=loader.load()
#     return documents

# documents=load_pdf_files(data=DATA_PATH)
# # print("Length of PDF pages: ", len(documents))


# # Step 2: Create Chunks
# def create_chunks(extracted_data):
#     text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,
#                                                  chunk_overlap=50)
#     text_chunks=text_splitter.split_documents(extracted_data)
#     return text_chunks

# text_chunks=create_chunks(extracted_data=documents)
# #print("Length of Text Chunks: ", len(text_chunks))

# # Step 3: Create Vector Embeddings 

# def get_embedding_model():
#     embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     return embedding_model

# embedding_model=get_embedding_model()

# # Step 4: Store embeddings in FAISS
# DB_FAISS_PATH="vectorstore/db_faiss"
# db=FAISS.from_documents(text_chunks, embedding_model)
# db.save_local(DB_FAISS_PATH)

# ((((((((((((((((((((((((((((((((perfectly fine for pdf only))))))))))))))))))))))))))))))))















#working fine but not for more pdf and curropted also 
# from langchain_community.document_loaders import (
#     PyPDFLoader,
#     TextLoader,
#     DirectoryLoader
# )

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS


# DATA_PATH = "data/"   # Put BOTH pdf and txt inside this folder


# # Step 1: Load PDF files
# def load_pdf_files(data):
#     pdf_loader = DirectoryLoader(
#         data,
#         glob="*.pdf",
#         loader_cls=PyPDFLoader
#     )
#     return pdf_loader.load()


# # Step 2: Load TXT files
# def load_txt_files(data):
#     txt_loader = DirectoryLoader(
#         data,
#         glob="*.txt",
#         loader_cls=TextLoader
#     )
#     return txt_loader.load()


# # Load both
# pdf_documents = load_pdf_files(DATA_PATH)
# txt_documents = load_txt_files(DATA_PATH)

# # Combine them
# documents = pdf_documents + txt_documents

# print("Total documents loaded:", len(documents))

# def create_chunks(extracted_data):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=800,
#         chunk_overlap=150
#     )
#     text_chunks = text_splitter.split_documents(extracted_data)
#     return text_chunks

# text_chunks = create_chunks(documents)
# print("Total chunks:", len(text_chunks))

# def get_embedding_model():
#     embedding_model = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )
#     return embedding_model

# embedding_model = get_embedding_model()

# DB_FAISS_PATH = "vectorstore/db_faiss"

# db = FAISS.from_documents(text_chunks, embedding_model)
# db.save_local(DB_FAISS_PATH)

# print("Vector store saved successfully!")





from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import glob

DATA_PATH = "data/"
DB_FAISS_PATH = "vectorstore/db_faiss"


# Step 1: Load PDF files one by one (skip corrupted ones)
def load_pdf_files(data):
    pdf_files = glob.glob(os.path.join(data, "*.pdf"))
    documents = []
    failed = []

    for i, pdf_path in enumerate(pdf_files, 1):
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            documents.extend(docs)
            if i % 100 == 0:
                print(f"  Loaded {i}/{len(pdf_files)} PDFs ({len(documents)} pages so far)...")
        except Exception as e:
            print(f"  [SKIP] Failed: {os.path.basename(pdf_path)} — {e}")
            failed.append(pdf_path)

    print(f"\nPDF loading done. Loaded: {len(pdf_files) - len(failed)}, Skipped: {len(failed)}")
    if failed:
        print("Failed files:")
        for f in failed:
            print(f"  - {f}")
    return documents


# Step 2: Load TXT files (skip bad ones)
def load_txt_files(data):
    txt_files = glob.glob(os.path.join(data, "*.txt"))
    documents = []
    failed = []

    for txt_path in txt_files:
        try:
            loader = TextLoader(txt_path, encoding="utf-8")
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"  [SKIP] Failed TXT: {os.path.basename(txt_path)} — {e}")
            failed.append(txt_path)

    print(f"TXT loading done. Loaded: {len(txt_files) - len(failed)}, Skipped: {len(failed)}")
    return documents


# Step 3: Chunk documents
def create_chunks(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return text_splitter.split_documents(extracted_data)


# Step 4: Build FAISS in batches (avoids memory issues with 1500 PDFs)
def build_faiss_in_batches(text_chunks, embedding_model, batch_size=500):
    os.makedirs(os.path.dirname(DB_FAISS_PATH), exist_ok=True)
    db = None

    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        print(f"  Embedding batch {i // batch_size + 1} ({i} to {i + len(batch)} chunks)...")

        if db is None:
            db = FAISS.from_documents(batch, embedding_model)
        else:
            batch_db = FAISS.from_documents(batch, embedding_model)
            db.merge_from(batch_db)  # Merge into main DB

    return db


# ── MAIN ──────────────────────────────────────────────────────────────────────

print("Loading PDFs...")
pdf_documents = load_pdf_files(DATA_PATH)

print("\nLoading TXTs...")
txt_documents = load_txt_files(DATA_PATH)

documents = pdf_documents + txt_documents
print(f"\nTotal documents loaded: {len(documents)}")

print("\nCreating chunks...")
text_chunks = create_chunks(documents)
print(f"Total chunks: {len(text_chunks)}")

print("\nLoading embedding model...")
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("\nBuilding vector store in batches...")
db = build_faiss_in_batches(text_chunks, embedding_model, batch_size=500)

db.save_local(DB_FAISS_PATH)
print("\nVector store saved successfully!")