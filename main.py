from agents.qa_agent import run_agent_for_folder

TECH_KEYWORDS = [
    "problem statement", "architecture", "methodology",
    "experimental results", "accuracy", "future scope", "limitations"
]

if __name__ == "__main__":
    run_agent_for_folder("Tech_docs", TECH_KEYWORDS)
