from tools.langgraph_qa import qa_graph
import os

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

if __name__ == "__main__":
    folder = "PM_docs"
    if not os.path.exists(folder):
        print(f"❌ Folder {folder} not found.")
        exit()

    result = qa_graph.invoke({
        "folder": folder,
        "keywords": PM_KEYWORDS,
        "file_list": None  # If you want to evaluate everything
    })

    print("✅ QA Completed. Results saved to `qa_results.csv`")
