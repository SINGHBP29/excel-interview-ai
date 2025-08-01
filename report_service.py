from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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
