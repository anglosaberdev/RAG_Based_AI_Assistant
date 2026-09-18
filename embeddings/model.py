
from langchain_huggingface import HuggingFaceEmbeddings

from constants import EMBEDDING_MODEL


def get_embedding_model():
    """
    Create and return the embedding model.
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

