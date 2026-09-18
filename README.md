# 🤖 RAG-Based AI Assistant

A modular **Retrieval-Augmented Generation (RAG) AI Assistant** built with **Python, LangChain, Chroma, Ollama, and Streamlit**.

The assistant retrieves relevant information from company policy documents and combines it with employee information and conversation history to generate contextual and personalized responses.

> **Note:** This project was built as a learning and engineering project while exploring practical RAG architecture, LangChain LCEL, vector databases, embeddings, and local LLMs.

---

## ✨ Features

* 📄 PDF document ingestion
* ✂️ Recursive document chunking
* 🧠 Dedicated embedding model
* 🗄️ Chroma vector database
* 🔎 Semantic retrieval using LangChain retrievers
* 🤖 Local LLM inference with Ollama
* 💬 Conversation history
* 👤 Employee-specific context
* 🧩 LangChain LCEL pipeline
* 🖥️ Streamlit chat interface
* ⚡ Streamlit caching for data and vector resources
* 🛡️ Error handling and logging
* 📦 Modular project structure

---

## 🏗️ Architecture

The application follows a modular RAG architecture:

```text
                    ┌─────────────────────┐
                    │   Company Policies  │
                    │        PDF          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PDF Loader       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Splitter     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Embedding Model   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Chroma Vector DB  │
                    └──────────┬──────────┘
                               │
                         Retrieval
                               │
                               ▼
User Query ───────────────► Retriever
                               │
                               ▼
                    Relevant Policy Context
                               │
                               ├──────────────┐
                               │              │
                               ▼              ▼
                     Employee Information   Chat History
                               │              │
                               └──────┬───────┘
                                      ▼
                            ┌─────────────────┐
                            │ ChatPromptTemplate│
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   Ollama LLM    │
                            │   Qwen3 1.7B    │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ StrOutputParser │
                            └────────┬────────┘
                                     │
                                     ▼
                              AI Response
```

---

## 🔄 RAG Workflow

### 1. Document Ingestion

The application loads the company policy PDF:

```text
umbrella_corp_policies.pdf
        ↓
     PDF Loader
        ↓
    Documents
```

### 2. Document Splitting

Large documents are divided into smaller chunks before embedding.

```text
Documents
    ↓
Text Splitter
    ↓
Document Chunks
```

Chunking improves retrieval by allowing the system to search smaller and more relevant pieces of information.

### 3. Embeddings

Each document chunk is converted into a vector representation using a dedicated embedding model.

```text
Document Chunk
      ↓
Embedding Model
      ↓
Vector Representation
```

These vectors are stored in Chroma.

### 4. Retrieval

When the user asks a question, the query is sent to the Chroma retriever.

```text
User Question
      ↓
Retriever
      ↓
Relevant Documents
```

The retrieved documents are then converted into a text context:

```python
"\n\n".join(
    doc.page_content for doc in docs
)
```

### 5. Prompt Construction

The retrieved policy information, employee information, conversation history, and current user input are combined into a `ChatPromptTemplate`.

```text
System Instructions
        +
Retrieved Policy Information
        +
Employee Information
        +
Conversation History
        +
Current User Input
        ↓
     Prompt
```

### 6. LLM Generation

The final prompt is passed to a local Ollama model.

```text
Prompt
  ↓
Ollama
  ↓
Qwen3 1.7B
  ↓
AI Response
```

---

## 🧠 LangChain LCEL Pipeline

One of the important parts of this project is the use of **LangChain Expression Language (LCEL)** to compose the RAG pipeline.

The chain can be represented as:

```text
                    ┌── Retriever ──► Policy Context
                    │
User Input ─────────┼── Passthrough ─► User Input
                    │
                    ├── History ─────► Conversation History
                    │
                    └── Employee ────► Employee Information
                                      │
                                      ▼
                              ChatPromptTemplate
                                      │
                                      ▼
                                     LLM
                                      │
                                      ▼
                               StrOutputParser
                                      │
                                      ▼
                                  Response
```

The core pipeline follows this pattern:

```python
(
    {
        "retrieved_policy_information": retriever,
        "user_input": RunnablePassthrough(),
        "conversation_history": lambda x: self.messages_history,
        "employee_information": lambda x: self.employee_information,
    }
    | prompt
    | self.llm
    | output_parser
)
```

This makes the data flow between the RAG components explicit and modular.

---

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
├── .env
└── README.md
```

### Module Responsibilities

| Module         | Responsibility                            |
| -------------- | ----------------------------------------- |
| `data/`        | Employee sample data and source documents |
| `ingestion/`   | PDF loading and document processing       |
| `embeddings/`  | Embedding model initialization            |
| `vectorstore/` | Chroma vector database creation           |
| `assistant.py` | RAG chain and conversation orchestration  |
| `llm.py`       | Local LLM configuration                   |
| `prompts.py`   | System prompt and welcome message         |
| `gui.py`       | Streamlit user interface                  |
| `app.py`       | Application entry point                   |

---

## 🛠️ Tech Stack

| Technology         | Purpose                              |
| ------------------ | ------------------------------------ |
| **Python**         | Application development              |
| **LangChain**      | LLM and RAG orchestration            |
| **LangChain LCEL** | Composing the processing pipeline    |
| **Chroma**         | Vector database                      |
| **Embeddings**     | Semantic representation of documents |
| **Ollama**         | Local LLM inference                  |
| **Qwen3 1.7B**     | Local language model                 |
| **Streamlit**      | Web interface                        |
| **PyPDF**          | PDF processing                       |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd RAG-Based-AI-Assistant
```

### 2. Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install and run Ollama

Make sure Ollama is installed and running.

Pull the Qwen3 model:

```bash
ollama pull qwen3:1.7b
```

Start Ollama if required:

```bash
ollama serve
```

Verify the model:

```bash
ollama list
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 💬 Example Interaction

```text
User:
How many vacation days do I have?

Assistant:
Based on the company policy and your employee information,
your available vacation balance is ...
```

The assistant uses both:

* Retrieved company policy information
* Employee-specific information

to generate the response.

---

## ⚡ Performance Considerations

The application uses Streamlit caching to avoid rebuilding expensive resources on every application rerun.

### Employee Data

```python
@st.cache_data(ttl=3600)
```

Used for caching generated employee data.

### Vector Store

```python
@st.cache_resource(ttl=3600)
```

Used for caching the Chroma vector store and avoiding repeated PDF processing and embedding operations.

This is particularly useful because document ingestion and embedding can be significantly more expensive than normal application execution.

---

## 🧩 Design Principles

This project follows several practical AI engineering principles:

### Modular Components

Each responsibility is isolated into its own module:

```text
Loading
   ↓
Splitting
   ↓
Embedding
   ↓
Vector Store
   ↓
Retrieval
   ↓
Prompt
   ↓
LLM
   ↓
Output
```

### Separation of Concerns

The application separates:

* Data generation
* Document ingestion
* Embeddings
* Vector storage
* LLM configuration
* Assistant orchestration
* UI rendering

This makes individual components easier to test, replace, and improve.

### Local LLM

The project uses Ollama instead of a hosted LLM API.

This makes it possible to experiment with RAG locally without sending application data to an external LLM provider.

---

## 🚧 Future Improvements

Possible next steps for the project:

* [ ] Add retrieval evaluation
* [ ] Add citation/source references to responses
* [ ] Add hybrid search
* [ ] Add metadata filtering
* [ ] Add reranking
* [ ] Add conversation summarization
* [ ] Add persistent chat history
* [ ] Add automated RAG evaluation
* [ ] Add unit and integration tests
* [ ] Add Docker support
* [ ] Add observability and tracing
* [ ] Add authentication and authorization
* [ ] Improve prompt management
* [ ] Add configurable chunk size and overlap
* [ ] Compare multiple embedding models

---

## 🙏 Credits & Learning Resource

A special thanks to the creator of the tutorial that helped guide the development and learning process behind this project.

🎥 **Tutorial:**
https://www.youtube.com/watch?v=WUUujm1MRQg

I used the tutorial as a learning reference to better understand how the different components of a practical RAG application can be connected together.

This project also represents my own hands-on implementation and experimentation with the architecture, code structure, and technologies used.

---

## 👨‍💻 About

This project is part of my ongoing journey in **Generative AI, RAG, LLM applications, and Agentic AI**, with a focus on understanding not only how to use frameworks, but also how the individual components communicate and work together.

**Built with Python • LangChain • Chroma • Ollama • Qwen3 • Streamlit**
