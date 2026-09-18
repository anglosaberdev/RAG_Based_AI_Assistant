from langchain_text_splitters import RecursiveCharacterTextSplitter

from constants import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents):
    """
    Split documents into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    splits = text_splitter.split_documents(documents)

    return splits
