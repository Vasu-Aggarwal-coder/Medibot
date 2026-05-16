# import os

# from langchain_groq import ChatGroq
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings

# from langchain import hub
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain

# # from dotenv import load_dotenv
# # load_dotenv()

# # Step 1: Setup Groq LLM
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# GROQ_MODEL_NAME = "llama-3.1-8b-instant"  # Change to any supported Groq model


# llm = ChatGroq(
#     model=GROQ_MODEL_NAME,
#     temperature=0.5,
#     max_tokens=512,
#     api_key=GROQ_API_KEY,
# )


# # Step 2: Connect LLM with FAISS and Create chain

# # Load Database
# DB_FAISS_PATH = "vectorstore/db_faiss"
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

# # Step 3: Build RAG chain
# retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# # Document combiner chain (stuff documents into prompt)
# combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

# # Retrieval chain (retriever + doc combiner)
# rag_chain = create_retrieval_chain(db.as_retriever(search_kwargs={'k': 3}), combine_docs_chain)



# # Now invoke with a single query
# user_query=input("Write Query Here: ")
# response=rag_chain.invoke({'input': user_query})
# print("RESULT: ", response["answer"])
# print("\nSOURCE DOCUMENTS:")
# for doc in response["context"]:
#     print(f"- {doc.metadata} -> {doc.page_content[:200]}...")











# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# from langchain_groq import ChatGroq
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # -------------------- Configuration --------------------
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY not found in environment variables!")

# GROQ_MODEL_NAME = "llama-3.1-8b-instant"
# DB_FAISS_PATH = "vectorstore/db_faiss"

# # -------------------- Initialize LLM --------------------
# print("Initializing Groq LLM...")
# llm = ChatGroq(
#     groq_api_key=GROQ_API_KEY,
#     model_name=GROQ_MODEL_NAME,
#     temperature=0.5,
#     max_tokens=512,
# )

# # -------------------- Load FAISS --------------------
# print("Loading vector database...")
# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# db = FAISS.load_local(
#     DB_FAISS_PATH, 
#     embedding_model, 
#     allow_dangerous_deserialization=True
# )

# # -------------------- Setup Retriever --------------------
# retriever = db.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 3}
# )

# # -------------------- Custom Prompt --------------------
# prompt_template = """Use the following pieces of context to answer the question at the end. 
# If you don't know the answer, just say that you don't know, don't try to make up an answer.

# Context: {context}

# Question: {question}

# Answer:"""

# prompt = PromptTemplate(
#     template=prompt_template, 
#     input_variables=["context", "question"]
# )

# # -------------------- Helper Functions --------------------
# def format_docs(docs):
#     """Format retrieved documents into a single string"""
#     return "\n\n".join(doc.page_content for doc in docs)

# # -------------------- Create RAG Chain --------------------
# print("Setting up RAG chain...")

# rag_chain = (
#     {
#         "context": retriever | format_docs,
#         "question": RunnablePassthrough()
#     }
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# # -------------------- Main Chat Loop --------------------
# if __name__ == "__main__":
#     print("\n" + "="*50)
#     print("RAG Chatbot Ready!")
#     print("="*50)
#     print("Type 'quit', 'exit', or 'q' to stop\n")
    
#     while True:
#         user_query = input("You: ").strip()
        
#         if user_query.lower() in ['quit', 'exit', 'q']:
#             print("Goodbye!")
#             break
        
#         if not user_query:
#             continue
        
#         try:
#             print("\nThinking...")
            
#             # Get retrieved documents using invoke (not get_relevant_documents)
#             docs = retriever.invoke(user_query)
            
#             # Get answer
#             answer = rag_chain.invoke(user_query)
            
#             print(f"\n🤖 Bot: {answer}\n")
            
#             # Show source documents
#             if docs:
#                 print("📚 Sources:")
#                 for i, doc in enumerate(docs, 1):
#                     source = doc.metadata.get('source', 'Unknown')
#                     page = doc.metadata.get('page', 'Unknown')
#                     print(f"  {i}. {source} - Page {page}")
#                 print()
            
#         except Exception as e:
#             print(f"\n❌ Error: {e}\n")
#             import traceback
#             traceback.print_exc()




































# without multilanguage support

# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# from langchain_groq import ChatGroq
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # -------------------- Configuration --------------------
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY not found in environment variables!")

# GROQ_MODEL_NAME = "llama-3.1-8b-instant"
# DB_FAISS_PATH = "vectorstore/db_faiss"

# # -------------------- Initialize LLM --------------------
# print("Initializing Groq LLM...")
# llm = ChatGroq(
#     groq_api_key=GROQ_API_KEY,
#     model_name=GROQ_MODEL_NAME,
#     temperature=0.5,
#     max_tokens=512,
# )

# # -------------------- Load FAISS --------------------
# print("Loading vector database...")
# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# db = FAISS.load_local(
#     DB_FAISS_PATH, 
#     embedding_model, 
#     allow_dangerous_deserialization=True
# )

# # -------------------- Setup Retriever --------------------
# retriever = db.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 3}
# )

# # -------------------- Custom Prompt --------------------
# prompt_template = """Use the following pieces of context to answer the question at the end. 
# If you don't know the answer, just say that you don't know, don't try to make up an answer.

# Context: {context}

# Question: {question}

# Answer:"""

# prompt = PromptTemplate(
#     template=prompt_template, 
#     input_variables=["context", "question"]
# )

# # -------------------- Helper Functions --------------------
# def format_docs(docs):
#     """Format retrieved documents into a single string"""
#     return "\n\n".join(doc.page_content for doc in docs)

# # -------------------- Create RAG Chain --------------------
# print("Setting up RAG chain...")

# rag_chain = (
#     {
#         "context": retriever | format_docs,
#         "question": RunnablePassthrough()
#     }
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# # -------------------- Main Chat Loop --------------------
# # This only runs when the script is executed directly
# if __name__ == "__main__":
#     print("\n" + "="*50)
#     print("RAG Chatbot Ready!")
#     print("="*50)
#     print("Type 'quit', 'exit', or 'q' to stop\n")
    
#     while True:
#         user_query = input("You: ").strip()
        
#         if user_query.lower() in ['quit', 'exit', 'q']:
#             print("Goodbye!")
#             break
        
#         if not user_query:
#             continue
        
#         try:
#             print("\nThinking...")
            
#             # Get retrieved documents using invoke
#             docs = retriever.invoke(user_query)
            
#             # Get answer
#             answer = rag_chain.invoke(user_query)
            
#             print(f"\n🤖 Bot: {answer}\n")
            
#             # Show source documents
#             if docs:
#                 print("📚 Sources:")
#                 for i, doc in enumerate(docs, 1):
#                     source = doc.metadata.get('source', 'Unknown')
#                     page = doc.metadata.get('page', 'Unknown')
#                     print(f"  {i}. {source} - Page {page}")
#                 print()
            
#         except Exception as e:
#             print(f"\n❌ Error: {e}\n")
#             import traceback
#             traceback.print_exc()
































#answer in all language 

import os
from dotenv import load_dotenv
from langdetect import detect
from deep_translator import GoogleTranslator

# Load env
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# -------------------- Config --------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found!")

GROQ_MODEL_NAME = "llama-3.1-8b-instant"
DB_FAISS_PATH = "vectorstore/db_faiss"

# -------------------- LLM --------------------
print("Initializing LLM..........")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL_NAME,
    temperature=0.5,
    max_tokens=512,
)

# -------------------- Embeddings --------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------- Load FAISS --------------------
print("Loading vector DB...........")

db = FAISS.load_local(
    DB_FAISS_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# -------------------- Prompt --------------------
prompt_template = """Use the context below to answer the question.

If answer not found, say you don't know.

Context:
{context}

Question:
{question}

Answer:"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# -------------------- Helper --------------------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# -------------------- RAG Chain --------------------
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# -------------------- Translator --------------------
def translate_to_english(text):
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text

def translate_from_english(text, target_lang):
    try:
        # deep-translator uses full language codes like "hi", "fr", "ar"
        # langdetect already returns these codes so no mapping needed
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception:
        return text

# -------------------- Multilingual Wrapper --------------------
def multilingual_rag(query):
    print("Detecting language...")
    try:
        lang = detect(query)
    except Exception:
        lang = "en"
    print("inside multilingual_rag inside connect_memory_with_llm.py")
    # Step 1: translate query to English
    query_en = translate_to_english(query) if lang != "en" else query

    docs = retriever.get_relevant_documents(query_en)
    #print(f"Retrieved {docs} documents for query: {query_en}")
    print("\n🔍 Retrieved Chunks:\n")
    for i, doc in enumerate(docs):
        print(f"----- Chunk {i+1} -----")
        print(doc.page_content)
        print("\n")

    # Step 2: run RAG in English
    answer_en = rag_chain.invoke(query_en)
    #print(f"RAG returned answer: {answer_en}\n(Original query: {query_en})")

    # Step 3: translate answer back to original language
    final_answer = translate_from_english(answer_en, lang) if lang != "en" else answer_en

    return final_answer, query_en


# -------------------- CLI Chat --------------------
if __name__ == "__main__":
    print("\n🌍 Multilingual Chatbot Ready!\n")

    while True:
        user_query = input("You: ").strip()

        if user_query.lower() in ["quit", "exit", "q"]:
            break

        if not user_query:
            continue

        try:
            print("\nThinking...")

            answer, query_en = multilingual_rag(user_query)
            docs = retriever.invoke(query_en)

            print(f"\n🤖 Bot: {answer}\n")

            if docs:
                print("📚 Sources:")
                for i, doc in enumerate(docs, 1):
                    source = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("page", "Unknown")
                    print(f"  {i}. {source} - Page {page}")
                print()

        except Exception as e:
            print("❌ Error:", e)