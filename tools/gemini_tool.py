from google import generativeai as genai

# Configure Gemini
genai.configure(api_key="AIzaSyBjHaLS_qURJ9g9ZQKPhsDrtLj5PpO2-C4")
model = genai.GenerativeModel("gemini-2.5-flash")

def evaluate_document_with_gemini(context_pairs):
    """
    Accepts keyword-context tuples and returns Gemini's QA feedback.
    """

    # ✅ Active prompt: Project Management QA (10-point checklist)
    prompt = f"""
You are a Project Management QA reviewer.

Below are keyword-based context snippets extracted from a PM document.
Your job is to assess whether the document addresses each of the following **compliance parameters**:

---

**Evaluation Checklist (1 point each):**

1. Is CRD updated and in sync with milestone data?
2. Were CSAT survey guidelines followed (survey name + customer contact)?
3. Was EPS tool used for design justification or documentation?
4. Was a Planning & Design call conducted, and were status/notes shared?
5. Were post-deployment checks completed (EPS lifecycle closure)?
6. Was formal closure communication sent to the customer (SCN/CAF)?
7. Was the customer kick-off meeting conducted and documented?
8. Is there a high-level project plan or schedule in an acceptable format?
9. Were risks/issues logged and communicated proactively?

---

For each parameter:
- Indicate if it is **Fully Present**, **Partially Addressed**, or **Missing**
- Give a **score (1 / 0.5 / 0)** depending on coverage
- Provide a short explanation or reference (if applicable)

Then:
- Return a **Total Score out of 9**
- Provide a final **Compliance Status**:
  - ✅ Compliant (score ≥ 8)
  - 🟡 Mostly Compliant (5–7.5)
  - ❌ Needs Improvement (below 5)
- Suggest 2–3 key improvement points if needed

---

**Context Extracted:**
{chr(10).join([f"Keyword: {k}\nContext: {c}" for k, c in context_pairs])}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {e}"



# 🧪 Old (commented out) prompt: Technical Document QA (4-point checklist)

#     prompt = f"""
# You are a QA reviewer for technical research documents.

# Based on the following extracted keyword-related content, evaluate whether the document contains:

# 1. A clearly explained problem statement
# 2. A proper architecture/methodology
# 3. Experimental results with discussion
# 4. Future scope or limitations

# For each, say if it's fully present, partially, or missing. Then give:
# - Grade each of them out of 1 and display it for each parameter
# - A score out of 4 (can be fractional)
# - Final status: Compliant / Mostly Compliant / Needs Improvement
# - Remarks for improvement

# Keyword Contexts:
# {chr(10).join([f"Keyword: {k}\nContext: {c}" for k, c in context_pairs])}
# """
