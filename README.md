# 🧠 Excel Interview Quiz — AI-Powered Mock Interview Platform

An intelligent, fully-automated Excel interview platform designed to streamline candidate assessment for recruiters. This AI-enhanced system dynamically generates questions, evaluates candidate responses in real-time using **Google Gemini**, and produces insightful performance summaries — all within a clean browser interface.

---

## 🚀 Live Deployment (Deploy Yourself)
 Live prject Link : https://singhbp29-excel-interview-ai-main-hd7ao4.streamlit.app/

> Easily deploy via:
```bash
streamlit run main.py

---

## 🧩 Table of Contents

* [🔍 Overview](#-overview)
* [🎯 Core Objectives](#-core-objectives)
* [🛠 Features](#-features)
* [🧠 AI & Product Engineering Contributions](#-ai--product-engineering-contributions)
* [👥 Candidate Workflow](#-candidate-workflow)
* [📊 Recruiter Dashboard](#-recruiter-dashboard)
* [📦 Project Structure](#-project-structure)
* [⚙️ Local Setup](#️-local-setup)
* [🛤 Future Enhancements](#-future-enhancements)
* [🧪 Sample Interviews](#-sample-interviews)
* [📄 License](#-license)

---

## 🔍 Overview

**Excel Interview Quiz** simulates a structured, AI-powered technical interview. It supports two distinct user flows:

* 👤 **Candidate**: Completes an adaptive Excel quiz and receives real-time AI feedback + report.
* 🧑‍💼 **Recruiter**: Reviews detailed submissions, feedback, and hiring-fit suggestions via a dashboard.

It ensures:

* Fair and dynamic evaluation
* Standardized performance metrics
* Objective recommendations for hiring

---

## 🎯 Core Objectives

| Core Requirement                | Implementation                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------- |
| 🧠 Structured Interview Flow    | Conversational multi-turn UI, question timing, and final summary                |
| 📈 Intelligent Evaluation       | Google Gemini evaluates answers with scoring and natural language feedback      |
| 🧠 Agentic Behavior             | The AI acts like an interviewer with expectations, timing, and scoring strategy |
| 📝 Constructive Feedback Report | PDF reports for both candidate and recruiter with a final recommendation        |

---

## 🛠 Features

### 👤 Candidate

* Login with name and email
* Receives 10 AI-generated Excel questions
* Adaptive timer per question based on complexity
* Real-time score + feedback from Gemini
* Submits mandatory post-quiz feedback
* Downloads personalized PDF performance report

### 🧑‍💼 Recruiter

* Secure login with password
* Sidebar to select any candidate
* See all responses, scores, and feedback
* View recommendation status ("Fit for Role")
* Download recruiter-view report in PDF format

---

## 🧠 AI & Product Engineering Contributions

### 🤖 AI Engineer

* Integrated Google Gemini 2.0 (Flash model)
* Developed prompts for diverse Excel topics
* Built:

  * `get_question()` — real-world scenario generation
  * `evaluate_answer()` — rubric-based scoring with feedback
* Tuned adaptive timer based on question complexity

### 🧪 AI Product Engineer

* Designed user journeys: quiz logic + state management
* Built multi-role login (candidate vs recruiter)
* Developed modular services:

  * `report_service.py` — PDF builder
  * `user_service.py` — session control
  * `leaderboard_service.py` — stores feedback
* Created clean recruiter dashboard in Streamlit
* Ensured feedback is mandatory before report access

---

## 👥 Candidate Workflow

1. Candidate logs in with name and email.
2. Receives 10 adaptive Excel questions.
3. Each question is timed (45–90 seconds).
4. After each answer, feedback + score is shown.
5. Once all 10 are done:

   * Final score displayed
   * Must submit feedback
   * Downloads PDF report with breakdown

---

## 📊 Recruiter Dashboard

1. Logs in securely (`recruiter123`)
2. Sidebar lists candidate sessions
3. On selection:

   * See all answers, scores, and comments
   * View feedback + "fit for role" recommendation
   * Download recruiter-version of report

---

## 📦 Project Structure

```
📁 excel-interview-quiz/
├── main.py                   # Streamlit app entrypoint
├── .env                      # API key storage
├── requirements.txt
│
├── 📁 data/                  # Stores candidate data + feedback
│
├── question_service.py       # Generates Excel questions
├── evaluation_service.py     # Scores & gives feedback using Gemini
├── report_service.py         # PDF generation logic
├── leaderboard_service.py    # Feedback + leaderboard logic
└── user_service.py           # Session init and storage
```

---

## ⚙️ Local Setup

### 1. Clone Repo

```bash
git clone https://github.com/yourusername/excel-interview-quiz.git
cd excel-interview-quiz
```

### 2. Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Gemini API Key

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the App

```bash
streamlit run main.py
```

---

## 🧪 Sample Interviews

Example:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "score": 42,
  "feedback": {
    "rating": 4,
    "comments": "Loved the flow! Some questions were tough.",
    "proceed": "Yes"
  },
  "fit_for_role": true
}
```

> Add screenshots or export sample JSONs if submitting as a portfolio project.

---

## 🛤 Future Enhancements

* ✅ Email candidate reports to recruiter automatically
* ✅ Tag questions by difficulty, topic, or role (HR, Analyst, PM)
* ✅ OTP-based email verification for candidates
* ✅ Admin dashboard with CSV export, analytics
* ✅ Multilingual question support

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

Have questions or want to contribute?

* 💌 `bhanups292004@gmail.com`
* 🤝 Open issues or PRs on GitHub

---
