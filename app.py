# Import the function used to generate sample employee data
from data.employees import generate_employee_data

# Load environment variables from the .env file
from dotenv import load_dotenv

# Streamlit is used to build the web-based user interface
import streamlit as st

# Used for working with JSON data
import json

# Load and process PDF documents
from ingestion.loader import load_pdf

# Split loaded documents into smaller chunks
from ingestion.splitter import split_documents

# Create/load the embedding model used for semantic search
from embeddings.model import get_embedding_model

# Create the Chroma vector store from document chunks and embeddings
from vectorstore.chroma import create_vectorstore

# Used to log errors and application information
import logging

# Import the system prompt and initial welcome message
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE

# Import the main Assistant class that coordinates the LLM, RAG, and user data
from assistant import Assistant

# Function used to initialize and return the LLM
from llm import get_llm

# Import the GUI class responsible for rendering the Streamlit interface
from gui import AssistantGUI  # Make sure the GUI module is available


# Run the application only when this file is executed directly
if __name__ == "__main__":

    # Configure the Streamlit page title and layout
    st.set_page_config(page_title="Welcome User", layout="wide")


    # Cache generated employee data for 1 hour
    # This prevents regenerating the same data on every Streamlit rerun
    @st.cache_data(ttl=3600, show_spinner="loading Spinner Data....")
    def get_user_data():

        # Generate one employee record and return the first employee
        return generate_employee_data(1)[0]


    # Cache the vector store for 1 hour
    # This avoids rebuilding the PDF embeddings and vector database
    # every time Streamlit reruns the application
    @st.cache_resource(ttl=3600, show_spinner="loading Vector Store....")
    def init_vector_store(pdf_path):

        try:
            # Load the PDF and convert it into documents
            documents = load_pdf(pdf_path)

            # Split the documents into smaller chunks
            # These chunks will later be embedded and stored in Chroma
            chunks = split_documents(documents)

            # Initialize the embedding model used to convert text into vectors
            embedding_model = get_embedding_model()

            # Create the Chroma vector store from the document chunks
            # and their corresponding embeddings
            vectorstore = create_vectorstore(
                documents=chunks,
                embedding_model=embedding_model,
            )

            # Return the initialized vector store
            return vectorstore

        except Exception as e:

            # Log the error for debugging purposes
            logging.error(f"Error initializing Vector Store: {str(e)}")

            # Display the error message in the Streamlit interface
            st.error(f"Error initializing Vector Store: {str(e)}")

            # Return None so the application can handle the failure gracefully
            return None


    # Initialize the employee information in Streamlit session state
    # only if it does not already exist
    if "customer" not in st.session_state:

        # Generate and store one employee record
        st.session_state.customer = get_user_data()


    # Initialize the conversation history in session state
    # only when the application starts for the first time
    if "messages" not in st.session_state:

        # Add the initial AI welcome message to the conversation
        st.session_state.messages = [
            {"role": "ai", "content": WELCOME_MESSAGE}
        ]


    # Initialize the vector store using the company policy PDF
    # This PDF provides the knowledge base for the RAG system
    vector_store = init_vector_store(
        "data/umbrella_corp_policies.pdf"
    )


    # Initialize the Large Language Model
    llm = get_llm()


    # Create the Assistant that coordinates:
    # - System instructions
    # - LLM
    # - Conversation history
    # - Vector store for RAG
    # - Employee information
    assistant = Assistant(
        system_prompt_str=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        vector_store_db=vector_store,
        employee_information=st.session_state.customer,
    )


    # Create the Streamlit GUI and connect it to the Assistant
    gui = AssistantGUI(assistant)

    # Render the user interface
    gui.render()