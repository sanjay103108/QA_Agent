import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

def save_results_to_csv(results, output_path="qa_results.csv"):
    """
    Saves a list of (filename, feedback) tuples to CSV.
    """
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Score", "Status", "Remarks"])
        for result in results:
            writer.writerow(result)

def parse_score_and_status(feedback_text):
    """
    Extracts score and compliance status from Gemini output.
    """
    score_match = re.search(r"score\s*[:=]?\s*([0-9.]+)", feedback_text, re.IGNORECASE)
    status_match = re.search(r"(Compliant|Mostly Compliant|Needs Improvement)", feedback_text, re.IGNORECASE)

    score = float(score_match.group(1)) if score_match else 0.0
    status = status_match.group(1) if status_match else "Unknown"

    return score, status

def send_alert_email(to_email, subject, body, sender_email, sender_password):
    """
    Sends a basic alert email via SMTP 
    """
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            print(f"Alert email sent to {to_email}")
    except Exception as e:
        print(f" Failed to send email: {e}")
