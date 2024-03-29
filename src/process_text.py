from sklearn.metrics.pairwise import cosine_similarity
import cohere
import numpy as np
import pandas as pd
import os
from src.retrieve_documents import download_patent_text


def return_embeddings(
    clean_text: list[str],
    input_type_embed="search_document",
    model_name="embed-english-v3.0",
) -> np.array:
    cohere_api_key = os.environ.get("cohere_api_key")
    co = cohere.Client(cohere_api_key)
    embeddings = co.embed(
        texts=clean_text, model=model_name, input_type=input_type_embed
    ).embeddings
    return embeddings


def return_most_relevant_passage(input_passage: str, patent_number: str) -> str:
    patent_df = return_patent(patent_number)
    passage_embedding = return_embeddings([input_passage])
    searched_patent_embeddings = return_embeddings(patent_df["clean_text"].to_list())
    similarities = cosine_similarity(passage_embedding, searched_patent_embeddings)
    most_relevant_passage_index = np.argmax(similarities)
    return patent_df.iloc[most_relevant_passage_index]["clean_text"]


def return_patent(patent_number: str) -> pd.DataFrame:
    patent_url = f"https://patents.google.com/patent/{patent_number}"
    patent_df = download_patent_text(patent_url)
    return patent_df


def summarize(text: str, prompt: str = "") -> str:
    cohere_api_key = os.environ.get("cohere_api_key")
    co = cohere.Client(cohere_api_key)
    response = co.summarize(
        text=text,
        extractiveness="low",
        format="paragraph",
        temperature=0.3,
        additional_command=prompt if len(prompt) > 1 else None,
    )
    return response.summary


def return_summary(patent_number: str, prompt: str = "") -> str:
    patent_df = return_patent(patent_number)
    text = " ".join(patent_df.clean_text.to_list())
    summary = summarize(text, prompt)
    return summary
