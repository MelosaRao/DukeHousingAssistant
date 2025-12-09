import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

# Define the HTML tags we want to extract
bs4_strainer = bs4.SoupStrainer(["p", "h1", "h2", "h3", "ul", "ol", "li"])

persistent_directory = os.path.join(os.getcwd(), "faiss_db_housing")


# Check if database already exists before rebuilding
local_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
if not os.path.exists(persistent_directory):
    print("Initializing vector store...")
    # Load multiple webpages with tag-based filtering
    loader = WebBaseLoader( 
        web_paths = [
            'https://students.duke.edu/living/housing/housing-assignments/spring-housing', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/durham-ordinances-and-policies/', 
            'https://students.duke.edu/living/housing/student-leadership/resident-program-assistant/', 
            'https://students.duke.edu/living/housing/housing-assignments/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/what-to-bring-and-what-not-to/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/furniture/', 
            'https://students.duke.edu/living/housing/first-year-housing/frequently-asked-questions/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/get-involved/', 
            'https://students.duke.edu/living/housing/dukecard/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#WannamakerInfo', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/landlord-tenant-issues/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/gps-300-swift/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/what-to-expect-in-residence-halls/', 
            'https://students.duke.edu/living/housing/housing-assignments/fall24-housing/', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#KilgoInfo', 
            'https://students.duke.edu/living/housing/upperclass-housing/upperclass-floor-plans/', 
            'https://students.duke.edu/living/housing/student-leadership/resident-assistants/#main-content', 
            'https://students.duke.edu/living/housing/student-leadership/', 
            'https://students.duke.edu/living/housing/hrl-team/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#main-content', 
            'https://students.duke.edu/living/housing/housing-assignments/#AllGender', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#CrowellInfo', 
            'https://students.duke.edu/living/housing/upperclass-housing/faqs/', 
            'https://students.duke.edu/living/housing/upperclass-housing/new-to-duke/', 
            'https://students.duke.edu/living/housing/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/for-undergraduates/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/duke-good-neighbor-program/#main-content', 
            'https://students.duke.edu/living/housing/housing-assignments/#NeedHelp', 
            'https://students.duke.edu/living/housing/student-leadership/julie-anne-levey/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/gps-300-swift/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/', 
            'https://students.duke.edu/living/housing/housing-assignments/spring-housing/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#KeohaneInfo', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/budgeting/', 
            'https://students.duke.edu/living/housing/student-leadership/councils/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/common-questions/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/subsidized-off-campus-housing/#main-content', 
            'https://students.duke.edu/living/housing/contact-us/', 
            'https://students.duke.edu/living/housing/housing-assignments/frequently-asked-questions/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/common-questions/ombuds@duke.edu', 
            'https://students.duke.edu/living/housing/student-leadership/residence-life-leaders/', 
            'https://students.duke.edu/living/housing/quadex/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/safety/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/shopping-for-groceries/', 
            'https://students.duke.edu/living/housing/student-leadership/residence-life-leaders/#main-content', 
            'https://students.duke.edu/living/housing/amenities-services/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/durham-neighborhoods/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/upperclass-floor-plans/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/llcs/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/utilities/', 
            'https://students.duke.edu/living/housing/first-year-housing/fy-housing-application/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/', 
            'https://students.duke.edu/living/housing/first-year-housing/fy-housing-application/', 
            'https://students.duke.edu/living/housing/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/off-campus-party/', 
            'https://students.duke.edu/living/housing/housing-assignments/spring-housing/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/durham-life/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#CravenInfo', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#HollowsInfo', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/for-undergraduates/', 
            'https://students.duke.edu/living/housing/first-year-housing/indoor-air-quality/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/budgeting/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/duml-housing/#main-content', 
            'https://students.duke.edu/living/housing/housing-assignments/spring-housing#main-content', 
            'https://students.duke.edu/living/housing/quadex/quad-cup/', 
            'https://students.duke.edu/living/housing/first-year-housing/east-campus-houses/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/shopping-for-groceries/#main-content', 
            'https://students.duke.edu/living/housing/annual-housing-calendar/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/durham-neighborhoods/', 
            'https://students.duke.edu/living/housing/housing-assignments/#2324License', 
            'https://students.duke.edu/living/housing/hrl-team/', 
            'https://students.duke.edu/living/housing/upperclass-housing/llcs/', 
            'https://students.duke.edu/living/housing/student-leadership/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/schools-childcare/', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#SwiftInfo', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/utilities/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/transportation/#main-content', 
            'https://students.duke.edu/living/housing/annual-housing-calendar/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/durham-life/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/roommates/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/living-on-east-campus/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/east-campus-houses/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/off-campus-party/#main-content', 
            'https://students.duke.edu/living/housing/student-leadership/resident-program-assistant/#main-content', 
            'https://students.duke.edu/living/housing/amenities-services/#main-content', 
            'https://students.duke.edu/living/housing/housing-assignments/frequently-asked-questions/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/roommates/', 
            'https://students.duke.edu/living/housing/first-year-housing/what-to-bring-and-what-not-to/', 
            'https://students.duke.edu/living/housing/upperclass-housing/faqs/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/transportation/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/safety/#main-content', 
            'https://students.duke.edu/living/housing/residence-life-policies/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/what-to-expect-in-residence-halls/#main-content', 
            'https://students.duke.edu/living/housing/quadex/quad-cup/#main-content', 
            'https://students.duke.edu/living/housing/quadex/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#FewInfo', 
            'https://students.duke.edu/living/housing/upperclass-housing/', 
            'https://students.duke.edu/living/housing/upperclass-housing/quad-descriptions/#EdensInfo', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/subsidized-off-campus-housing/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/roommates/#main-content', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/common-questions/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/duke-good-neighbor-program/', 
            'https://students.duke.edu/living/housing/housing-assignments/#AssignPol', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/roommates/', 
            'https://students.duke.edu/living/housing/housing-assignments/#2324Rates', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/schools-childcare/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/get-involved/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/frequently-asked-questions/', 
            'https://students.duke.edu/living/housing/student-leadership/councils/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/furniture/#main-content', 
            'https://students.duke.edu/living/housing/residence-life-policies/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/#main-content', 
            'https://students.duke.edu/living/housing/contact-us/#main-content', 
            'https://students.duke.edu/living/housing/first-year-housing/living-on-east-campus/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/durham-ordinances-and-policies/#main-content', 
            'https://students.duke.edu/living/housing/upperclass-housing/new-to-duke/#main-content', 
            'https://students.duke.edu/living/housing/housing-assignments/', 
            'https://students.duke.edu/living/housing/first-year-housing/indoor-air-quality/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/landlord-tenant-issues/#main-content', 
            'https://students.duke.edu/living/housing/dukecard/', 
            'https://students.duke.edu/living/housing/student-leadership/julie-anne-levey/', 
            'https://students.duke.edu/living/housing/student-leadership/resident-assistants/', 
            'https://students.duke.edu/living/housing/first-year-housing/', 
            'https://students.duke.edu/living/housing/graduate-professional-housing/housing-in-durham/duml-housing/'
        ],

        bs_kwargs={"parse_only": bs4_strainer} )

    docs = loader.load()

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(
        all_splits, embedding=local_embeddings
    )
    vectorstore.save_local("./faiss_db_housing")
else:
    print("Loading existing vector store...")
    vectorstore = FAISS.load_local("./faiss_db_housing", embeddings=local_embeddings,allow_dangerous_deserialization=True)




#test retrieval and LLM response
question = "Can you tell me about laundry at Duke?"
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
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