from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.llms.base import LLM
from tools.file_tools import read_all_documents
from tools.keyword_extractor import extract_keyword_contexts
from tools.gemini_tool import evaluate_document_with_gemini

from tools.output_tools import (
    parse_score_and_status,
    send_alert_email,
    save_results_to_csv
)


def run_agent_for_folder(folder_path, keywords, file_list=None):
    docs = read_all_documents(folder_path)
    output = ""
    results = []

    for filename, content in docs.items():
        if file_list and filename not in file_list:
            continue

        context = extract_keyword_contexts(content, keywords)
        if context:
            output += f"\n📄 Evaluating: {filename}\n\n"
            result = evaluate_document_with_gemini(context)
            output += result + "\n\n"

            score, status = parse_score_and_status(result)
            results.append((filename, score, status, result.replace("\n", " ")))

            if score < 2.5:
                send_alert_email(
                    to_email="seshadri.mamatha@gmail.com",
                    subject=f"QA Alert for {filename}",
                    body=f"Score: {score}\nStatus: {status}\n\n{result}",
                    sender_email="sanjay10.seshadri@gmail.com",
                    sender_password="divt xebz zwhx ervs"
                )
        else:
            output += f"\n⚠️ No relevant content found in {filename}\n\n"

    # Optional: save to CSV
    save_results_to_csv(results)

    return output


# def run_agent_for_folder(folder_path, keywords, file_list=None):
#     docs = read_all_documents(folder_path)
#     output = ""
#     for filename, content in docs.items():
#         if file_list and filename not in file_list:
#             continue  # skip unrelated files
#         context = extract_keyword_contexts(content, keywords)
#         if context:
#             output += f"\n📄 Evaluating: {filename}\n\n"
#             result = evaluate_document_with_gemini(context)
#             output += result + "\n\n"
#         else:
#             output += f"\n⚠️ No relevant content found in {filename}\n\n"
#     return output

