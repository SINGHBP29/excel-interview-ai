import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def generate_excel_question():
    prompt = (
        "Generate a challenging but clear Excel-related interview question for a candidate. "
        "Focus on formulas, data analysis, charts, or pivot tables."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

def evaluate_answer(question, answer):
    prompt = f"""
    You are an expert Excel interviewer. Evaluate the candidate's answer below.

    Question: {question}
    Answer: {answer}

    Rate the answer from 0 to 5 and give brief feedback. Respond in JSON format:
    {{
        "score": <number>,
        "feedback": "<your feedback>"
    }}
    """
    response = model.generate_content(prompt)
    
    try:
        import json
        result = json.loads(response.text.strip())
        return result["score"], result["feedback"]
    except Exception as e:
        return 0, f"Failed to parse response: {str(e)}"
