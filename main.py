from tools.file_tools import read_all_documents
from tools.keyword_extractor import extract_keyword_contexts
from tools.gemini_tool import evaluate_document_with_gemini
from tools.output_tools import (
    parse_score_and_status,
    save_results_to_csv,
    send_alert_email,
)

# TECH_KEYWORDS = [
#     "problem statement", "architecture", "methodology",
#     "experimental results", "accuracy", "future scope", "limitations"
# ]

PM_KEYWORDS = [
    "CRD update", "Go-Live date", "deployment timeline", "revised milestone",
    "CSAT survey", "customer feedback", "survey project name", "client contact",
    "EPS tool", "design justification", "EPS lifecycle", "field-level mapping",
    "planning call", "design meeting", "status notes", "architecture review",
    "post-deployment check", "QA validation", "cutover checklist", "EPS closure",
    "closure email", "CAF", "SCN", "handoff complete",
    "kick-off meeting", "project launch", "scope alignment",
    "project plan", "Gantt chart", "milestone tracker", "high-level schedule",
    "resource request", "Merlin", "staffing plan",
    "risk log", "issue tracker", "escalation", "RAG status"
]

# Is CRD updated and is in sync with milestone data
# CSAT - Verify if survey Project Name and Customer Contact is updated
# Check if Post Deployment checks have been completed
# Check if closure communication has been sent to the customer
# Verify if design was created using EPS tool
# Check if Planning and Design call conducted, status sent and notes updated

ALERT_EMAIL = "seshadri.mamatha@gmail.com"
SENDER_EMAIL = "sanjay10.seshadri@gmail.com"
SENDER_PASSWORD = "divt xebz zwhx ervs"

if __name__ == "__main__":
    docs = read_all_documents("PM_docs")
    results = []

    for filename, content in docs.items():
        print(f"\n Evaluating: {filename}")
        context = extract_keyword_contexts(content, PM_KEYWORDS)

        if not context:
            print(" No relevant content found.")
            continue

        feedback = evaluate_document_with_gemini(context)
        print(" Feedback:\n", feedback)

        score, status = parse_score_and_status(feedback)
        results.append((filename, score, status, feedback.replace("\n", " ")))

        if score < 2.5:
            send_alert_email(
                to_email=ALERT_EMAIL,
                subject=f" QA Alert for {filename}",
                body=f"Score: {score}\nStatus: {status}\n\n{feedback}",
                sender_email=SENDER_EMAIL,
                sender_password=SENDER_PASSWORD
            )

    save_results_to_csv(results)
    print(" All results saved to qa_results.csv")
