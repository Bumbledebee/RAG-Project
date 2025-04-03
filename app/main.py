import streamlit as st
import os
import time
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
import openai
import chromadb
import utils

# --- Load API keys ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
#api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="Test Your Statistics Knowledge", page_icon="📊", layout="wide")

# --- Initialize Session State for Responses ---
if "answer" not in st.session_state:
    st.session_state["answer"] = ""

# --- Header with Logo & Title in Two Columns ---
col1, col2 = st.columns([2, 2])

with col1:
    st.image("images/statistics_quiz.png", width=400)

with col2:
    st.title("Gain Confidence Today")
    st.subheader("Prepare for your next test with us. On the go and at home.")
    # --- User Input ---
    user_question = st.text_input("What is your question?")

    if user_question:
        # --- Start Timer ---
        start_time = time.time()

        with st.spinner("The answer is being prepared..."):
            document_dir = "./"
            pdf_file = "data/Introduction to Statistics.pdf"

            @st.cache_resource
            def checking_database():
                """Loads the PDF, splits it into chunks, and creates vector embeddings."""
                file_path = os.path.join(document_dir, pdf_file)
                pdf_content = utils.load_pdf(file_path)
                cleaned_content = utils.clean_pdf(pdf_content)
                documents = [Document(page_content=text) for text in cleaned_content]
                embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
                client = chromadb.PersistentClient(path="./chroma_db")
                db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db", client=client)
                return db

            db = checking_database()
            retrieved_docs = db.similarity_search(user_question, k=10)

            if retrieved_docs:
                source_info = "[Book link](https://stats.libretexts.org/Bookshelves/Introductory_Statistics/Introductory_Statistics_(Shafer_and_Zhang)/01%3A_Introduction_to_Statistics)"
                context_text = retrieved_docs[0].page_content
            else:
                source_info = ""
                context_text = "No context available."

            # --- Construct AI Prompt ---
            prompt = f"""
            ## SYSTEM ROLE
            You are a Statistics Professor answering to students' questions.

            ## USER QUESTION
            "{user_question}"

            ## CONTEXT
            '''
            {context_text}
            '''

            ## RESPONSE FORMAT
            **Answer:** [Concise response]

            **Key Points:**
            - Bullet point 1
            - Bullet point 2

            {source_info}
            """

            # --- Call OpenAI GPT ---
            client = openai.OpenAI()
            model_params = {
                'model': 'gpt-4o',
                'temperature': 0.5,
                'max_tokens': 3000,
                'top_p': 0.9,
                'frequency_penalty': 0.5,
                'presence_penalty': 0.6
            }

            messages = [{'role': 'user', 'content': prompt}]
            completion = client.chat.completions.create(messages=messages, **model_params, timeout=120)
            st.session_state["answer"] = completion.choices[0].message.content

        # --- End Timer ---
        end_time = time.time()
        elapsed_time = end_time - start_time

        # --- Display AI Response and Time Taken ---
        st.markdown(f"{st.session_state['answer']}")
        st.markdown(f"*Processing Time in Seconds: {elapsed_time:.2f}*")