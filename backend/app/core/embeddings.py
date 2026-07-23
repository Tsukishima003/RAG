import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings


def create_embeddings():
    api_key = os.getenv("HF_API_TOKEN")
    if not api_key:
        raise ValueError(
            "Missing Hugging Face API token. Set HF_API_TOKEN in your .env / "
        )
    return HuggingFaceInferenceAPIEmbeddings(
        api_key=api_key,
        model_name="BAAI/bge-m3",
    )