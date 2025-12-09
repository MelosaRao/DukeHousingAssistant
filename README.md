# DukeHousingAssistant
## About
This project implements a fully functional Retrieval-Augmented Generation (RAG) system designed to serve as an intelligent Duke Housing Assistant. The system automatically crawls and extracts high-quality text from dozens of official Duke housing webpages, preprocesses and tokenizes the content, and stores it in a FAISS vector database using semantic sentence embeddings. When a user asks a question, the system performs semantic similarity search to retrieve the most relevant housing information and then sends this context to a state-of-the-art language model (Google Gemini) to generate accurate, grounded responses with proper citations. The final application is deployed through an interactive Gradio chatbot interface, allowing students to ask open-ended or specific housing questions and receive detailed, reliable, and source-linked answers in real time.

Some important files:
- extract_database.py: use web scraping to gather all required URLs for RAG database
- rag.py: builds faiss_db_housing using the above URLs if it does not exists and test it with sample query. 
- app.py main file which when run lauches gradio UI. Contains code for entire chatbot app with multiconversaton system and history tracking.
-test_rag.py: Test a query by replacing the question variable and running this files. Allows for test without running chatbot. 
- Custom_text.py: allows you to add custom_text to the database by replacing custom_text and custom_source variables with appropriate values.

## Quick Start
Click on this link to do to the web deployed version on hugging face: https://huggingface.co/spaces/Melosa/DukeHousingAsssistant

Quick Note: If you are running on hugging face please open the links to webpages in a new tab. It generally opens in the new tab automatically. But if it tries to open in the same tab as hugging face chatbot window it might have some issues. This is nothing to do with the codebase just how hugging face is hosted I believe.

Also hugging face setup uses my api key which has rate limits. If you want to ask a lot of questions please set up locally with your own api key.

(you might have to wait a few minutes for it to initialise and then you can chat with the chatbot) 

Or to setup locally: 
- clone the repo on your machine and navigate to the repo directory.
- Then set up virtual environment and activate virtual  using terminal. Here is the code to do that for windows. For mac or linux the code varies slightly. Setup according to your os.

'python -m venv venv'
'venv\Scripts\activate'

- Next on your terminal write 'pip install -r requirements.txt'
- Create a .env file in the project root containing: GOOGLE_API_KEY=your_api_key_here (You will need a google api key here. Its free to create on https://ai.google.dev/gemini-api/docs/api-key. )
- Then on terminal run 'run python app.py' to launch the chatbot locally.

## Video Links
- demo: https://drive.google.com/file/d/15f5HihP7Q7JMpGtELcJKtzFi_RH7x7FJ/view?usp=sharing
- technical walkthrough:https://drive.google.com/file/d/1yizRbXiA8iTplbW5fErJJJXSnEVxXQSv/view?usp=sharing


## Prompt Engineering Evaluation
Results are included in prompt-analysis.csv. I tried 3 differnt prompts (with id 1,2,3).

After testing all three prompts, I decided to keep the first one because it consistently gives the most helpful and complete answers. It follows the exact format I asked for, including the “Answer:” section and the list of sources at the end. This is important for my project since I want the chatbot to always show where its information is coming from. The first prompt also tends to give more detailed explanations, which works better for a housing assistant where extra clarity and context are useful for students.

The second prompt technically gives correct answers, but it almost never includes sources, even though it was told to. Because of that, it doesn’t really fit the needs of this application. The third prompt does follow the instructions, but the responses are a bit shorter and not as informative. They still work, just not as well as the first prompt. Overall, the first prompt gives the most consistent output and the best user experience, so that’s why I chose to keep it.

## Qualitative and Quantitative Evaluation of Results
To evaluate my chatbot, I compared the chat responses to my expected answers both qualitatively and quantitatively. My results are in 'evaluation.csv'. Qualitatively, most answers were accurate—for example, the model correctly explained Edens dorm, identified the RC of Randolph, and followed instructions when information wasn’t available. I gave every response a score between 1-5. 1 if it was completely wrong as compared to my answer and 5 when it had all the details. I used 4 as a score when certain details were missing in the response that would add to the explaination like for where is hollows it correctly said it was on west campus but if it gave a location reference like i did in my expected answer that it was on west campus and near edens it would have been better.

For a score of 2 it has few correct details but misses a lot, for 3 it gets about half the details like for the last result. It got correct details for RA eligibility 'To be eligible for an RA position, a candidate must have a 2.5 cumulative GPA and be in good standing with the University. Applicants must also be able to begin the RA/CA role in Spring 2026 or August 2026.' but it also missed a some of my points 'RAs and CAs must be full-time enrolled, degree-seeking students in good academic standing at Duke University and must maintain a cumulative 2.5 GPA while in their position. Undergraduate, graduate, and professional degree students are eligible for the RA and CA positions. 
RAs and CAs may not enroll in more than five (5) units, per semester without approval from their supervisor. 
RAs and CAs must also remain in good conduct and disciplinary standing with the university at all times. This includes adhering to all University and Housing & Residence Life policies as outlined in the Duke Community Standard Guide and Housing License. 
Must be willing to adhere to all positional conditions and expectations outlined in the position description.'
Overall over 15 queries the average score was 4.4/5 which is pretty high and suggest in my qualitative evaluation the chatbot is doing good.

For a quantitative metric, I used semantic similarity with sentence embeddings, which gives a score between 0 and 1 based on meaning rather than exact wording. This gives a more reliable measure of how close the model's answer is to the expected answer. Check 'quantitative_evaluation.ipynb' for details.

After running the semantic similarity evaluation between my expected answers and the model’s chat responses, the average similarity score came out to 0.7059. A score of 1 would mean the answers are nearly identical in meaning, while 0 would mean they are totally unrelated. So a score of around 0.70 shows that, on average, the model is capturing most of the intended meaning, even if it phrases things differently or adds extra context. This lines up with what I saw qualitatively: the chatbot usually gives the right information, but sometimes adds more detail or words things in a slightly different way. Overall, a similarity score of ~0.71 indicates that the model is performing well and staying close to the expected responses.

Another good thing about this is that in tries to retain context for example from the evaluation.csv you can see that these two were back to back question and answers:
- question: i need help with mailing packages
- answer: For assistance with mailing packages at Duke, Duke Campus Mail Services offers various resources. You can learn how to properly address mail and packages for on-campus students. For parcels requiring special handling or for perishable items, specific information is available. If you need to track down a missing or delayed package, guidance is provided. You can also find out how mail enters the Duke Campus Mail system and how you will be notified when your packages are ready for pick up. The Student Mailbox Center service window is available for packages that are too large to fit into a standard mailbox. Additionally, information regarding forwarding mail and parcels is also provided. 

Sources:

https://students.duke.edu/living/housing/amenities-services/
https://students.duke.edu/living/housing/amenities-services/#main-content
https://students.duke.edu/living/housing/first-year-housing/frequently-asked-questions/#main-content
https://students.duke.edu/living/housing/first-year-housing/frequently-asked-questions/

- question: what address do i use for this. I live in blackwell
- answer: The address to use for Blackwell is 51 Brodie Gym Drive. You would also include your Box Number, Residence Hall, and Room Number on Address Line 2.


Question context is infered from the one before it knows that it needs to give the mailing address


## Edge cases
- When asked information that the model does not know it should reply -> 'I'm not sure. I cannot find the information in the provided documents but if there are some matching sources I will list them below.' And this behavior is consistent with its replies when asked questions like 'who is brandon fain'- something the model has no knowlegde of (check evaluation.csv result 3)

- When gave it an objectively wrong statement (check evaluation.csv result 4) like "freshmen stay on west campus and others stay on east campus". I expected it to refute and say something like no freshmen stay on east campus. While it did not negate my false statement it did provide the correct information 'First-year students live on East Campus and have automatic membership into an affiliated West Campus Quad. Sophomores then move to live in their connected West Campus Quad.'. 

Overall the model seems to be less prone to hallucination and states clearly if something is not present in the database which is a positive. When presented with false information it replies with the correct information. This is good for model accuracy though refuting the information strongly with a 'no' ot 'this is incorrect' would be a good addition.

### Features Implemented
- Collected or constructed original dataset through substantial engineering effort (e.g., API integration, web scraping, manual annotation/labeling, custom curation) with documented methodology (10 pts) (see extract_database.ipynb data was scraped from duke website and then vector database was created and saved in rag.py as FAISS vector database)

- Implemented comprehensive text preprocessing and tokenization pipeline (3 pts) (see rag.py lines 10 to 166 
implemented a full text-preprocessing and tokenization pipeline that includes HTML tag-level filtering using BeautifulSoup, removal of non-content elements, and structured document extraction from multiple webpages. The cleaned text is then segmented using a RecursiveCharacterTextSplitter with controlled chunk size and overlap, which acts as tokenization windowing process.
)

- Applied prompt engineering with evaluation of multiple prompt designs (evidence: comparison table) (3 pts yes see README top for dicussion on this.)

- Used sentence embeddings for semantic similarity or retrieval (5 pts yes i used HuggingFaceEmbeddings - all-MiniLM-L6-v2 and similarity search 'retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})' see rag.py and app.py)

- Made API calls to state-of-the-art model (GPT-4, Claude, Gemini) with meaningful integration into your system (5 pts yes see rag.py and app.py specificalyy lines 20 -99 from app.py. 
'llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)' 
called on the llm and gave it the query output and the question and it gives out an answer in my desired format which is then returned to ui.)

- Built multi-turn conversation system with context management and history tracking (7 pts see see app.py this keeps track of chat_history and provides this as context to llm. Also uses gradio application to make sure chat history is visible to user in UI and its a chatbot interface is used to develop a multi conversation system.)

- Built retrieval-augmented generation (RAG) system with document retrieval (e.g., from a static dataset/database, or from dynamic web search/scraping) and generation components (10 pts see see rag.py basically build FAISS database faiss_db_housing in rag.py. See app.py query_rag function which hadles generation.)

- Used a significant software framework for applied ML not covered in the class (e.g., instead of PyTorch, used Tensorflow; or used JAX, LangChain, etc. not covered in the class) (5 pts yes see app,py and rag.py I used Langchain framework for generating vector store (rag.py) and quering it. Also I acesss Gemini api through langchain framework.).

- Deployed model as functional web application with user interface (10 pts yes see app.py where a gradio interface is used. Deployed on hugging face link on top of 'README.md' and 'SETUP.md')

- Completed project individually without a partner (10 pts)

- Analyzed model behavior on edge cases or out-of-distribution examples (5 pts see README top for evaluation)
- Conducted both qualitative and quantitative evaluation with thoughtful discussion (5 pts see README top for evaluation)