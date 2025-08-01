import streamlit as st
import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv
from question_service import get_question
from evaluation_service import evaluate_answer
from report_service import generate_report
from user_service import init_session
from leaderboard_service import update_leaderboard

# Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
st.set_page_config(page_title="🧠 Excel Interview Quiz", layout="centered")

# Initialize session
init_session(st)
session = st.session_state.session

# UI
st.title("📘 Excel Interview Quiz")
login_type = st.sidebar.selectbox("Login as", ["Candidate", "Recruiter"])

if login_type == "Candidate":
    st.subheader("Candidate Login")
    st.markdown("Welcome! I'm your **AI Excel Interviewer**. You'll answer 10 practical Excel questions. Each has a time limit. At the end, you'll receive a score and personalized feedback.")

    session["name"] = st.text_input("Full Name", session.get("name", ""))
    session["email"] = st.text_input("Email", session.get("email", ""))

    if session["name"] and session["email"]:
        if session.get("completed"):
            st.warning("You have already completed this quiz.")
            st.stop()

        if len(session["data"]) < 10:
            question = get_question(session, model)

            def get_timer_seconds(question_text):
                q = question_text.lower()
                if any(k in q for k in ["basic", "true", "shortcut"]):
                    return 45
                elif any(k in q for k in ["sum", "filter", "vlookup", "function"]):
                    return 60
                else:
                    return 90

            timer_seconds = get_timer_seconds(question)
            st.subheader(f"Question {len(session['data']) + 1}/10")
            st.write(f"🧠 **Question:** {question}")

            if "timer_start" not in session:
                session["timer_start"] = time.time()

            time_elapsed = int(time.time() - session["timer_start"])
            time_left = max(0, timer_seconds - time_elapsed)
            st.info(f"⏳ Time left: {time_left} seconds")

            if time_left > 0:
                answer = st.text_area("Your Answer", disabled=False)
                if st.button("Submit Answer"):
                    score, feedback = evaluate_answer(model, question, answer)
                    st.success(f"✅ Score: {score}/5")
                    st.info(f"💬 Feedback: {feedback}")

                    session["data"].append({
                        "question": question,
                        "answer": answer,
                        "score": score,
                        "feedback": feedback
                    })
                    session["score"] += score
                    del session["timer_start"]
                    st.rerun()
            else:
                st.warning("⏰ Time's up! You cannot submit an answer.")
                answer = st.text_area("Your Answer", disabled=True)
                if st.button("Continue"):
                    session["data"].append({
                        "question": question,
                        "answer": "",
                        "score": 0,
                        "feedback": "No answer submitted (timeout)"
                    })
                    del session["timer_start"]
                    st.rerun()
        else:
            session["completed"] = True
            st.success("🎉 Interview Completed!")
            st.write(f"🏁 **Total Score:** {session['score']} / 50")

            # 💾 Save data for recruiter
            session_file = os.path.join(DATA_FOLDER, f"{session['email']}.json")
            with open(session_file, "w") as f:
                json.dump(session, f, indent=2)

            # 📄 Generate report
            file_name = os.path.join(DATA_FOLDER, f"{session['email']}_report.pdf")
            generate_report(file_name, session["name"], "Candidate", session["data"], session["score"])

            # Feedback
            st.subheader("📋 Feedback")
            rating = st.slider("Rate your experience:", 1, 5, 3)
            comments = st.text_area("Suggestions or feedback")
            proceed = st.radio("Do you recommend this candidate for the role?", ["Yes", "No", "Maybe"])

            if st.button("Submit Feedback"):
                session["feedback"] = {
                    "rating": rating,
                    "comments": comments,
                    "proceed": proceed
                }
                update_leaderboard(session)

                feedback_file = os.path.join(DATA_FOLDER, f"{session['email']}_feedback.json")
                with open(feedback_file, "w") as f:
                    json.dump(session, f, indent=2)

                st.success("Thank you for your feedback!")

                with open(file_name, "rb") as f:
                    st.download_button("⬇️ Download Report", f, file_name="report.pdf")
                os.remove(file_name)

                with open(feedback_file, "rb") as f:
                    st.download_button("⬇️ Download Feedback Data", f, file_name="feedback.json")
                os.remove(feedback_file)

elif login_type == "Recruiter":
    st.subheader("Recruiter Dashboard")
    password = st.text_input("Enter Recruiter Password", type="password")
    if password != "recruiter123":
        st.warning("Incorrect password.")
        st.stop()

    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json") and not f.endswith("_feedback.json")]
    selected_email = st.sidebar.selectbox("Select Candidate", files, format_func=lambda x: x.replace(".json", ""))

    if selected_email:
        file_path = os.path.join(DATA_FOLDER, selected_email)
        with open(file_path) as f:
            data = json.load(f)

        if not data.get("completed"):
            st.info("Candidate has not completed the quiz yet.")
        else:
            st.markdown("---")
            st.write(f"**Name:** {data['name']}")
            st.write(f"**Email:** {data['email']}")
            st.write(f"**Score:** {data.get('score', 0)} / 50")

            feedback = data.get("feedback")
            if feedback:
                st.subheader("📩 Candidate Feedback")
                st.write(f"**Experience Rating:** {feedback.get('rating')}/5")
                st.write(f"**Comments:** {feedback.get('comments')}")
                st.write(f"**Hiring Recommendation:** {feedback.get('proceed')}")
            else:
                st.info("No feedback submitted by candidate.")

            report_name = os.path.join(DATA_FOLDER, f"{data['email']}_recruiter_report.pdf")
            generate_report(report_name, data['name'], "Recruiter", data["data"], data.get("score", 0))
            with open(report_name, "rb") as f_pdf:
                st.download_button("Download Report", f_pdf, file_name="recruiter_report.pdf", key=data["email"])
            os.remove(report_name)
