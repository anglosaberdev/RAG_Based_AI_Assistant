from langchain_ollama import ChatOllama

def get_llm():

    return ChatOllama(
        model="qwen3:1.7b",
        base_url="http://localhost:11434",
        temperature=0.3
    )