from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple
from tools.file_tools import extract_text_from_file
from tools.keyword_extractor import extract_keyword_contexts
from tools.gemini_tool import evaluate_document_with_gemini
from tools.output_tools import parse_score_and_status, send_alert_email
from tools.constants import PM_KEYWORDS, TECH_KEYWORDS
import os

# Define LangGraph state
class GraphState(TypedDict):
    filename: str
    content: str
    context: List[Tuple[str, str]]
    feedback: str
    score: float
    status: str

# Step 1: Extract raw text
def extract_text_node(state: GraphState) -> GraphState:
    text = extract_text_from_file(state["filename"])
    return {**state, "content": text or ""}

# Step 2: Extract context using keywords
def extract_context_node(state: GraphState) -> GraphState:
    keywords = PM_KEYWORDS if "PM_docs" in state["filename"] else TECH_KEYWORDS
    context = extract_keyword_contexts(state["content"], keywords)
    return {**state, "context": context}

# Step 3: Evaluate document
def evaluate_node(state: GraphState) -> GraphState:
    feedback = evaluate_document_with_gemini(state["context"])
    return {**state, "feedback": feedback}

# Step 4: Score document
def scoring_node(state: GraphState) -> GraphState:
    score, status = parse_score_and_status(state["feedback"])
    return {**state, "score": score, "status": status}

# Step 5: Email alert if score is bad
def alert_node(state: GraphState) -> GraphState:
    if state["score"] < 2.5:
        send_alert_email(
            to_email="seshadri.mamatha@gmail.com",
            subject=f"QA Alert: {os.path.basename(state['filename'])}",
            body=f"Score: {state['score']}\nStatus: {state['status']}\n\n{state['feedback']}",
            sender_email="sanjay10.seshadri@gmail.com",
            sender_password="divt xebz zwhx ervs"
        )
    return state

# Define graph builder
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

qa_graph = build_langgraph_qa_graph()
