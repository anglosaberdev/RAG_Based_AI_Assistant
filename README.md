# 🤖 RAG-Based AI Assistant

A modular **Retrieval-Augmented Generation (RAG) AI Assistant** built with Python and Streamlit.

The application allows users to interact with an AI assistant that can retrieve relevant information from company policy documents and generate contextual responses using an LLM.

## 🚀 Features

* 📄 PDF document ingestion
* ✂️ Document chunking and text splitting
* 🧠 Custom embedding model
* 🗄️ Chroma vector database
* 🔎 Semantic search and retrieval
* 🤖 LLM-powered responses
* 👤 Employee information integration
* 💬 Conversation history
* 🖥️ Streamlit-based chat interface
* ⚡ Streamlit caching for better performance
* 🧩 Modular project architecture

## 🏗️ RAG Pipeline

```text
PDF Documents
      ↓
Document Loader
      ↓
Text Splitter
      ↓
Embedding Model
      ↓
Chroma Vector Store
      ↓
User Query
      ↓
Semantic Retrieval
      ↓
Relevant Context
      ↓
LLM
      ↓
AI Assistant Response
```

## 📁 Project Structure

```text
RAG-Based-AI-Assistant/
│
├── data/
│   ├── employees.py
│   └── umbrella_corp_policies.pdf
│
├── ingestion/
│   ├── loader.py
│   └── splitter.py
│
├── embeddings/
│   └── model.py
│
├── vectorstore/
│   └── chroma.py
│
├── assistant.py
├── gui.py
├── llm.py
├── prompts.py
├── app.py
├── requirements.txt
└── README.md
```

## 🛠️ Technologies

* Python
* Streamlit
* LangChain
* Chroma
* Embeddings
* Large Language Models (LLMs)
* Retrieval-Augmented Generation (RAG)
