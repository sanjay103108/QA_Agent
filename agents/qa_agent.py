from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.llms.base import LLM
from tools.file_tools import read_all_documents
from tools.keyword_extractor import extract_keyword_contexts
from tools.gemini_tool import evaluate_document_with_gemini

# def run_agent_for_folder(folder_path, keywords):
#     docs = read_all_documents(folder_path)
#     for filename, content in docs.items():
#         context = extract_keyword_contexts(content, keywords)
#         if context:
#             print(f"\nEvaluating {filename}...\n")
#             result = evaluate_document_with_gemini(context)
#             print(result)
#         else:
#             print(f"\nNo relevant content found in {filename}")

def run_agent_for_folder(folder_path, keywords, file_list=None):
    docs = read_all_documents(folder_path)
    output = ""
    for filename, content in docs.items():
        if file_list and filename not in file_list:
            continue  # skip unrelated files
        context = extract_keyword_contexts(content, keywords)
        if context:
            output += f"\n📄 Evaluating: {filename}\n\n"
            result = evaluate_document_with_gemini(context)
            output += result + "\n\n"
        else:
            output += f"\n⚠️ No relevant content found in {filename}\n\n"
    return output

