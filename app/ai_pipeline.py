import os
import fitz  # PyMuPDF
import docx
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with your key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text(filepath):
    """Extracts raw text from PDF or DOCX files."""
    ext = filepath.split('.')[-1].lower()
    text = ""
    try:
        if ext == 'pdf':
            with fitz.open(filepath) as doc:
                for page in doc:
                    text += page.get_text()
        elif ext == 'docx':
            doc_file = docx.Document(filepath)
            text = "\n".join([para.text for para in doc_file.paragraphs])
        return text
    except Exception as e:
        print(f"Extraction Error: {e}")
        return ""

def audit_contract(text, user_context):
    """Sends text to Gemini and returns a structured JSON audit."""
    prompt = f"""
    You are ContractHawk, a professional legal AI auditor. 
    User Context for this audit: {user_context}
    
    TASK: Analyze the provided contract text for high-risk clauses.
    1. Identify the 3 most predatory or risky clauses.
    2. Assign a Risk Score (1-100) to each.
    3. Provide a 'Neutralized Version' (fair, standard replacement text).
    4. Provide a 'Plain English' explanation of why the original was dangerous.

    IMPORTANT: Return the response ONLY as a valid JSON list. No conversational text.
    Format:
    [
      {{
        "clause": "original text",
        "risk": 85,
        "fix": "neutralized text",
        "explanation": "why it is risky"
      }}
    ]

    Contract Content:
    {text[:10000]} 
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean potential markdown formatting from AI response
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return clean_json
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "[]"
