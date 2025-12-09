from langchain_core.documents import Document
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()

#test retrieval and LLM response replace question below to test different queries
question = "Tell me the quad connection for Bell Tower?"
persistent_directory = os.path.join(os.getcwd(), "faiss_db_housing")

local_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(persistent_directory, embeddings=local_embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
retrieved_docs = retriever.invoke(question)


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
context = ' '.join([f"Source: {doc.metadata['source']}\n{doc.page_content}" for doc in retrieved_docs])

response = llm.invoke(f"""
Please provide an answer based only on the provided context. 
- If the user asks an open-ended question, respond in detail (100-120 words). 
- If it is a specific question, respond briefly (1-2 sentences). 
- If the answer is not found in the context, respond with 'I'm not sure'.
- At the end of your response, list the sources in a formatted way.

Question: {question}.
Context: {context}

Format Example:
Answer: [Generated Response]
Sources:
1. [URL1]
2. [URL2]
""")

print(response.content)