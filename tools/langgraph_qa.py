from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple
from tools.file_tools import extract_text_from_file
from tools.keyword_extractor import extract_keyword_contexts
from tools.gemini_tool import evaluate_document_with_gemini
from tools.output_tools import parse_score_and_status, send_alert_email
from tools.constants import PM_KEYWORDS, TECH_KEYWORDS
import re


# Updated GraphState with recipient_email
class GraphState(TypedDict):
    filename: str
    content: str
    context: List[Tuple[str, str]]
    feedback: str
    score: float
    status: str
    recipient_email: str


# Step 1: Extract text and recipient email
def extract_text_node(state: GraphState) -> GraphState:
    text = extract_text_from_file(state["filename"]) or ""

    # Extract email using regex from the document text
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    recipient_email = email_match.group(0) if email_match else ""

    return {**state, "content": text, "recipient_email": recipient_email}


# Step 2: Extract keyword context
def extract_context_node(state: GraphState) -> GraphState:
    from tools.constants import PM_KEYWORDS, TECH_KEYWORDS  # Safer import
    keywords = PM_KEYWORDS if "PM_docs" in state["filename"] else TECH_KEYWORDS
    context = extract_keyword_contexts(state["content"], keywords)
    return {**state, "context": context}


# Step 3: Evaluate with Gemini
def evaluate_node(state: GraphState) -> GraphState:
    feedback = evaluate_document_with_gemini(state["context"])
    return {**state, "feedback": feedback}


# Step 4: Parse score and status
def scoring_node(state: GraphState) -> GraphState:
    score, status = parse_score_and_status(state["feedback"])
    return {**state, "score": score, "status": status}


# Step 5: Trigger alert if score is low and email is found
def alert_node(state: GraphState) -> GraphState:
    if state["score"] < 7:
        if state["recipient_email"]:
            send_alert_email(
                to_email=state["recipient_email"],
                subject=f"QA Alert: {state['filename']}",
                body=f"Score: {state['score']}\nStatus: {state['status']}\n\n{state['feedback']}",
                sender_email="sanjay10.seshadri@gmail.com",
                sender_password="divt xebz zwhx ervs"
            )
            print(f"Alert sent to {state['recipient_email']}")
        else:
            print(f"No email found in {state['filename']}, skipping alert.")
    return state


# LangGraph builder function
def build_langgraph_qa_graph():
    builder = StateGraph(GraphState)
    builder.add_node("extract_text", extract_text_node)
    builder.add_node("extract_context", extract_context_node)
    builder.add_node("evaluate", evaluate_node)
    builder.add_node("score", scoring_node)
    builder.add_node("alert", alert_node)

    builder.set_entry_point("extract_text")
    builder.add_edge("extract_text", "extract_context")
    builder.add_edge("extract_context", "evaluate")
    builder.add_edge("evaluate", "score")
    builder.add_edge("score", "alert")
    builder.add_edge("alert", END)

    return builder.compile()


# Final graph object
qa_graph = build_langgraph_qa_graph()
