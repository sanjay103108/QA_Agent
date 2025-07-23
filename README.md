This project is a Document Quality Assurance (QA) Checker that uses LangGraph's agentic workflow to assess compliance and completeness of uploaded Project Management or Technical Documents.

It performs the following steps via agents: 

Extracts text from uploaded .pdf, .docx, or .txt documents

Detects relevant keyword-context pairs

Evaluates compliance using Google's Gemini AI model

Scores the document (Compliant / Mostly Compliant / Needs Improvement)

Sends alert emails automatically for low-quality documents

