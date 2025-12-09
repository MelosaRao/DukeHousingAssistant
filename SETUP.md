Web Version (Hugging Face)

Click the link below to open the deployed chatbot:
Hugging Face Space Link

Note: The application may take 1–3 minutes to initialize if it is sleeping.

Local Installation

Follow the steps below to run the chatbot locally.

1. Clone the Repository using github ('git clone ...' You can choose to use ssh or https options depending on your setup) and then nagivate into the repo using 'cd <REPO_NAME>'

If you do not have Git installed, download the ZIP version of the repository and extract it, then navigate into the extracted folder.

2. Create and Activate a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate

macOS / Linux
python3 -m venv venv
source venv/bin/activate

Once activated, you should see (venv) at the start of your terminal prompt.

3. Install Dependencies
pip install -r requirements.txt

4. Add Environment Variables. You will need a google api key here. Its free to create on https://ai.google.dev/gemini-api/docs/api-key. 

Create a .env file in the project root containing.:

GOOGLE_API_KEY=your_api_key_here


5. Launch the Chatbot
Windows
python app.py

macOS / Linux
python3 app.py


A link like the following will appear:

Running on http://127.0.0.1:7860/


Click the link to open the chatbot in your browser.