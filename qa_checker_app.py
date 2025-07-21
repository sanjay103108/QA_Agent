import streamlit as st
import os
from tools.langgraph_qa import qa_graph


from tools.constants import PM_KEYWORDS, TECH_KEYWORDS


st.set_page_config(page_title="Document QA Checker", layout="centered")
st.title("Automated Quality Assurance")

# Category
doc_type = st.radio("Select document category:", ("PM_docs", "Tech_docs"))


uploaded_files = st.file_uploader(
    f"Upload files to {doc_type}",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)


if uploaded_files:
    folder = doc_type
    os.makedirs(folder, exist_ok=True)

    for uploaded_file in uploaded_files:
        filepath = os.path.join(folder, uploaded_file.name)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button(f"Run QA Evaluation for {uploaded_file.name}", key=uploaded_file.name):
            st.info("Processing... This may take a few seconds")
            result = qa_graph.invoke({"filename": filepath})
            st.success("QA Evaluation Completed!")
            st.subheader("Evaluation Results:")
            st.markdown(result.get("feedback", "No feedback available."))
