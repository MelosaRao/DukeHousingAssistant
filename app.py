import gradio as gr
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set. Please add it as a secret in your Hugging Face Space.")

# Load vectorstore
persistent_directory = os.path.join(os.getcwd(), "faiss_db_housing")
local_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(persistent_directory, local_embeddings, allow_dangerous_deserialization=True)


# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Initialize chat history
system_prompt = SystemMessage(content="You are a helpful AI Housing assistant of Duke University Students.")
chat_history = [system_prompt]

# Core RAG function
def query_rag(user_input, history):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 8})
    docs = retriever.invoke(user_input)
    context = "\n\n".join([f"{doc.page_content}\n(Source: {doc.metadata.get('source', 'unknown')})" for doc in docs])

    prompt = (f"""Please provide an answer based only on the provided context. 
            - If the user asks an open-ended question, respond in detail (100-120 words). 
            - If it is a specific question, respond briefly (1-2 sentences). 
            - If the answer is not found in the context, respond with 'I'm not sure. I cannot find the information in the provided documents but if there are some matching sources I will list them below.'.
            - At the end of your response, list the sources in a formatted way.

            Question: {user_input}.
            Context: {context}

            Format Example:
            Answer: [Generated Response]
            Sources:
            1. [URL1]
            2. [URL2]
            """
    )



    chat_history.append(HumanMessage(content=prompt))
    response = llm.invoke(chat_history)
    chat_history.append(HumanMessage(user_input))
    chat_history.append(AIMessage(content=response.content))
    return response.content

#gradio interface
gr.ChatInterface(
    fn=query_rag,
    title="<span style='font-size: 2.2em;'>Duke Housing Assistant</span>",
    description="<span style='font-size: 1.3em; color: #4b5563;'>Ask me anything about Duke housing — dorms, roommates, policies, and more.</span>",
   examples=[
            "What’s included in Edens dorm?",
            "How do I do laundry at Duke?",
            "What is QuadEx?"
        ],
    chatbot=gr.Chatbot(),
    submit_btn="  📤  Send  "


).launch()