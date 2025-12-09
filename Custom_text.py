from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
# Define your custom text & source
custom_text = """The quad connections are as follows:
- Basset and Pegram have quad connections with Craven.
- Giles and Wilson have quad connections with Crowell.
- Bell Tower and Trinity have quad connections with Edens.
- Gilbert-Addoms(GA) and Southgate have quad connections with Few.
- Blackwell and Randolph have quad connections with Keohane.
- Alspaugh and Brown have quad connections with Kilgo.
- East House and West House have quad connections with Wannamaker."""

custom_source = "https://students.duke.edu/living/housing/first-year-housing/frequently-asked-questions/"
# Create document with metadata
custom_doc = Document(page_content=custom_text, metadata={"source": custom_source})
persistent_directory = os.path.join(os.getcwd(), "faiss_db_housing")
local_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(persistent_directory, embeddings=local_embeddings, allow_dangerous_deserialization=True)
# Add document with embeddings
vectorstore.add_documents([custom_doc])
print(f"Document added to vectorstore with source: {custom_source}")