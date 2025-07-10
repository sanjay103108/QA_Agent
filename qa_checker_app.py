import streamlit as st
import os
from agents.qa_agent import run_agent_for_folder

# Set up page
st.set_page_config(page_title="Document QA Checker", layout="centered")
st.title("📄 Project Document QA Checker")

# Step 1: Choose document type
doc_type = st.radio("Select document category:", ("PM_docs", "Tech_docs"))

# Step 2: Upload files
uploaded_files = st.file_uploader(
    f"Upload files to {doc_type}",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

file_names = []

if uploaded_files:
    folder = doc_type
    os.makedirs(folder, exist_ok=True)

    for uploaded_file in uploaded_files:
        filepath = os.path.join(folder, uploaded_file.name)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_names.append(uploaded_file.name)

    st.success(f"✅ Uploaded {len(uploaded_files)} file(s) to `{folder}`")

# Step 3: Run QA on uploaded files
if uploaded_files and st.button("🔍 Run QA Evaluation"):
    st.info("Processing... This may take a few seconds ⏳")

    if doc_type == "PM_docs":
        keywords = [
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
    else:
        keywords = [
            "problem statement", "architecture", "methodology",
            "experimental results", "accuracy", "future scope", "limitations"
        ]

    results = run_agent_for_folder(folder, keywords, file_list=file_names)
    st.success("✅ QA Evaluation Completed!")

    st.subheader("📋 Evaluation Results:")
    st.text(results if results else "No results to show.")
