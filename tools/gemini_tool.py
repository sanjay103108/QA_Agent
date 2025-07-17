from google import generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-1.5-flash")

def evaluate_document_with_gemini(context_pairs):
    """
    Accepts keyword-context tuples and returns Gemini's QA feedback.
    """
    prompt = f"""
You are a QA reviewer for technical research documents.

Based on the following extracted keyword-related content, evaluate whether the document contains:

1. A clearly explained problem statement
2. A proper architecture/methodology
3. Experimental results with discussion
4. Future scope or limitations

For each, say if it's fully present, partially, or missing. Then give:
- Grade each of them out of 1 and display it for each parameter
- A score out of 4 (can be fractional)
- Final status: Compliant / Mostly Compliant / Needs Improvement
- Remarks for improvement

Keyword Contexts:
{chr(10).join([f"Keyword: {k}\nContext: {c}" for k, c in context_pairs])}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API Error: {e}"
