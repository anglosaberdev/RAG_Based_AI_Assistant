from langchain_chroma import Chroma

from constants import VECTOR_STORE_PATH


def create_vectorstore(documents, embedding_model):
    """
    Create and persist a Chroma vector store.
    """

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )

    return vectorstore
