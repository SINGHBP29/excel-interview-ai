import google.generativeai as genai
from utils import safe_generate_content

QUESTION_CATEGORIES = [
    "Excel formulas and functions",
    "Excel data analysis",
    "Excel charts and visualization",
    "Excel pivot tables",
    "Excel shortcuts and efficiency",
    "Excel error handling",
    "Conditional formatting",
    "Data cleaning techniques in Excel",
    "Case studies using Excel",
    "Excel VBA and macros"
]

# def generate_excel_question(model, topic):
#     prompt = f"""
#     Generate one technical Excel interview question on: "{topic}".
#     It should test real-world skill. Avoid definitions and theory.
#     """
#     return model.generate_content(prompt).text.strip()

def generate_excel_question(model, topic):
    prompt = f"""
Generate one technical Excel interview question on the topic: "{topic}".
Avoid definitions. Focus on practical, real-world skills.
"""
    return safe_generate_content(model, prompt)

def get_question(session_data, model):
    index = len(session_data["data"]) % len(QUESTION_CATEGORIES)
    topic = QUESTION_CATEGORIES[index]
    return generate_excel_question(model, topic)
