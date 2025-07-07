from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.llms.base import LLM
from tools.file_tools import read_all_documents
from tools.keyword_extractor import extract_keyword_contexts
from tools.gemini_tool import evaluate_document_with_gemini

def run_agent_for_folder(folder_path, keywords):
    docs = read_all_documents(folder_path)
    for filename, content in docs.items():
        context = extract_keyword_contexts(content, keywords)
        if context:
            print(f"\n🔍 Evaluating {filename}...\n")
            result = evaluate_document_with_gemini(context)
            print(result)
        else:
            print(f"\n⚠️ No relevant content found in {filename}")
