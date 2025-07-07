import re

def extract_keyword_contexts(text, keywords, window=2):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    contexts = []
    for i, sentence in enumerate(sentences):
        for kw in keywords:
            if kw.lower() in sentence.lower():
                start = max(i - window, 0)
                end = min(i + window + 1, len(sentences))
                context = " ".join(sentences[start:end])
                contexts.append((kw, context))
    return contexts
