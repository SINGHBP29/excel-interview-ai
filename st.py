# import streamlit as st
# from question_service import get_question
# from evaluation_service import evaluate_answer
# from report_service import generate_report
# import uuid
# import os
# import json
# from datetime import datetime

# DATA_FOLDER = "data"
# os.makedirs(DATA_FOLDER, exist_ok=True)

# st.set_page_config(page_title="🧠 Excel Interview Quiz", layout="centered")

# # -------------------- Utility Functions --------------------
# def load_user(email):
#     filepath = os.path.join(DATA_FOLDER, f"{email}.json")
#     if os.path.exists(filepath):
#         with open(filepath, "r") as f:
#             return json.load(f)
#     return None

# def save_user(data):
#     filepath = os.path.join(DATA_FOLDER, f"{data['email']}.json")
#     with open(filepath, "w") as f:
#         json.dump(data, f, indent=2)

# # -------------------- App Entry --------------------
# st.title("📘 Excel Interview Quiz")

# login_type = st.sidebar.selectbox("Login as", ["Candidate", "Recruiter"])

# # -------------------- Candidate Flow --------------------
# if login_type == "Candidate":
#     st.subheader("Candidate Login")
#     name = st.text_input("Full Name")
#     email = st.text_input("Email")
#     contact = st.text_input("Contact Number")

#     existing_data = load_user(email) if email else None
#     if existing_data and existing_data.get("completed"):
#         st.warning("You've already submitted this quiz.")
#         st.stop()

#     if name and email and contact:
#         if "session" not in st.session_state:
#             st.session_state.session = {
#                 "user_id": str(uuid.uuid4()),
#                 "name": name,
#                 "email": email,
#                 "contact": contact,
#                 "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "q_index": 0,
#                 "data": [],
#                 "total_score": 0,
#                 "completed": False
#             }

#     session = st.session_state.get("session")
#     if session:
#         if session["q_index"] < 10:
#             question = get_question()
#             st.subheader(f"Question {session['q_index'] + 1}/10")
#             st.write(question)
#             user_answer = st.text_area("Your Answer")

#             if st.button("Submit Answer"):
#                 score, feedback = evaluate_answer(question, user_answer)
#                 st.success(f"Score: {score}/5")
#                 st.info(f"Feedback: {feedback}")

#                 session["data"].append({
#                     "question": question,
#                     "answer": user_answer,
#                     "score": score,
#                     "feedback": feedback
#                 })
#                 session["total_score"] += score
#                 session["q_index"] += 1
#                 st.rerun()
#         else:
#             session["completed"] = True
#             save_user(session)
#             st.success("🎉 Quiz Completed!")
#             st.write(f"Name: {session['name']}")
#             st.write(f"Email: {session['email']}")
#             st.write(f"Total Score: {session['total_score']}/50")

#             report_file = f"{session['user_id']}_report.pdf"
#             generate_report(report_file, session["name"], "Candidate", session["data"], session["total_score"])

#             with open(report_file, "rb") as f:
#                 st.download_button("⬇️ Download Your Report", f, file_name="candidate_report.pdf", mime="application/pdf")
#             os.remove(report_file)

#             # Feedback Form
#             st.subheader("🗒️ Your Feedback")
#             rating = st.slider("Rate your quiz experience:", 1, 5, 3)
#             comments = st.text_area("Suggestions or comments")
#             proceed = st.radio("Would you like to proceed with recruitment?", ["Yes", "No", "Maybe"])

#             if st.button("Submit Feedback"):
#                 session["candidate_feedback"] = {
#                     "rating": rating,
#                     "comments": comments,
#                     "proceed": proceed
#                 }
#                 save_user(session)
#                 st.success("Thank you! Your feedback has been submitted.")

# # -------------------- Recruiter Flow --------------------
# elif login_type == "Recruiter":
#     st.subheader("Recruiter Dashboard")
#     recruiter_pass = st.text_input("Enter Recruiter Password", type="password")
#     if recruiter_pass != "recruiter123":
#         st.stop()

#     files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]
#     for file in files:
#         with open(os.path.join(DATA_FOLDER, file), "r") as f:
#             data = json.load(f)
#             if not data.get("completed"):
#                 continue

#             st.markdown("---")
#             st.markdown(f"**Name:** {data['name']}")
#             st.markdown(f"**Email:** {data['email']}")
#             st.markdown(f"**Contact:** {data['contact']}")
#             st.markdown(f"**Start Time:** {data['start_time']}")
#             st.markdown(f"**Score:** {data['total_score']} / 50")

#             # Candidate Feedback
#             fb = data.get("candidate_feedback", {})
#             if fb:
#                 st.markdown("##### 📄 Candidate Feedback")
#                 st.write(f"**Rating:** {fb.get('rating')}/5")
#                 st.write(f"**Comments:** {fb.get('comments', 'N/A')}")
#                 st.write(f"**Willing to Proceed:** {fb.get('proceed')}")

#             report_file = f"{data['user_id']}_report.pdf"
#             generate_report(report_file, data["name"], "Recruiter", data["data"], data["total_score"])
#             with open(report_file, "rb") as f_pdf:
#                 st.download_button("⬇️ Download Report", f_pdf, file_name=f"{data['name']}_report.pdf", mime="application/pdf", key=data["email"])
#             os.remove(report_file)

#             # Recruiter Feedback
#             st.markdown("#### 📓 Recruiter Feedback")
#             feedback = st.text_area(f"Enter feedback for {data['name']}", key=f"fb_{data['email']}")
#             if st.button(f"Submit Feedback for {data['email']}", key=f"submit_{data['email']}"):
#                 data["recruiter_feedback"] = feedback
#                 save_user(data)
#                 st.success("Recruiter feedback saved.")

import os
import json
import time
import uuid
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in the .env file.")

# Configure Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Excel topics
QUESTION_CATEGORIES = [
    "Excel formulas and functions",
    "Excel data analysis",
    "Excel charts and visualization",
    "Excel pivot tables",
    "Excel shortcuts and efficiency",
    "Excel error handling",
    "Conditional formatting",
    "Data cleaning techniques in Excel"
]

# Real-life case studies
CASE_STUDIES = [
    {
        "title": "Sales Dashboard Case Study",
        "description": "You're given sales data for 12 months. Create a dashboard with total sales, trends, etc. What Excel tools would you use and why?"
    },
    {
        "title": "HR Attrition Analysis Case Study",
        "description": "You have employee data with age, department, salary, etc. How would you use Excel to explore attrition causes?"
    }
]

# Feedback and leaderboard support
LEADERBOARD_FILE = "leaderboard.json"

# Session Initialization
def init_session():
    if "session" not in st.session_state:
        st.session_state.session = {
            "id": str(uuid.uuid4()),
            "name": "",
            "email": "",
            "data": [],
            "feedback": {},
            "score": 0
        }

# Generate a question
def generate_excel_question(topic):
    prompt = f"""
    Generate one technical Excel interview question on: \"{topic}\".
    It should test real skill. Avoid definitions and theory.
    """
    return model.generate_content(prompt).text.strip()

# Evaluate answer
def evaluate_answer(question, answer):
    prompt = f"""
You are a senior Excel expert evaluating a candidate’s response to an Excel interview question.

Evaluate the candidate’s answer using these criteria:
1. **Accuracy**
2. **Clarity**
3. **Relevance**

### Question:
{question}

### Candidate Answer:
{answer}

Respond with strict JSON:
{{
  "score": <0 to 5>,
  "feedback": "<brief feedback>"
}}
"""
    response = model.generate_content(prompt)
    try:
        result = json.loads(response.text.strip())
        return result["score"], result["feedback"]
    except Exception as e:
        return 0, f"Error parsing Gemini response: {str(e)}"

# Generate report

def generate_report(filename, user_name, report_type, records, total_score):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"{report_type} Report for {user_name}")

    c.setFont("Helvetica", 12)
    y = height - 90

    for i, record in enumerate(records, 1):
        c.drawString(50, y, f"{i}. Q: {record['question']}")
        y -= 18
        if report_type == "Candidate":
            c.drawString(60, y, f"A: {record['answer']}")
            y -= 18
        c.drawString(60, y, f"Score: {record['score']}, Feedback: {record['feedback']}")
        y -= 24
        if y < 100:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total Score: {total_score} / {len(records) * 5}")
    c.save()

# Get question based on index
def get_question():
    index = len(st.session_state.session['data']) % len(QUESTION_CATEGORIES)
    topic = QUESTION_CATEGORIES[index]
    return generate_excel_question(topic)

# Save to leaderboard
def update_leaderboard():
    entry = {
        "name": st.session_state.session['name'],
        "email": st.session_state.session['email'],
        "score": st.session_state.session['score'],
        "date": str(datetime.now()),
        "feedback": st.session_state.session['feedback']
    }
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            board = json.load(f)
    else:
        board = []
    board.append(entry)
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=2)

# Run this with: streamlit run this_script.py
# if __name__ == '__main__':
#     st.warning("Please use the Streamlit app interface to run this script.")
