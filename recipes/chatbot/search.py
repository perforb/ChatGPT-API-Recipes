import os

import numpy as np
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from scipy import spatial

load_dotenv(find_dotenv())
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# https://github.com/openai/openai-python/blob/release-v0.28.1/openai/embeddings_utils.py#L139
def distances_from_embeddings(
        query_embedding: list[float],
        embeddings: list[list[float]],
        distance_metric="cosine",
) -> list[list]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances


def create_context(question, df: pd.DataFrame, max_len=1000) -> str:
    q_embeddings = client.embeddings.create(
        input=question,
        model="text-embedding-ada-002"
    ).data[0].embedding
    df["distances"] = distances_from_embeddings(
        q_embeddings,
        df["embeddings"].apply(eval).apply(np.array).values,
        distance_metric='cosine'
    )

    returns = []
    cur_len = 0

    for _, row in df.sort_values("distances", ascending=True).iterrows():
        cur_len += row["n_tokens"] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])

    return "\n\n###\n\n".join(returns)


def answer_question(question: str, conversation_history: list[dict]) -> str:
    df = pd.read_csv("embedding.csv")
    context = create_context(question, df, max_len=200)
    prompt = f"あなたはとあるホテルのスタッフです。コンテキストに基づいて、お客様からの質問に丁寧に答えてください。コンテキストが質問に対して回答できない場合は「わかりません」と答えてください。\n\nコンテキスト: {context}\n\n---\n\n質問: {question}\n回答:"
    conversation_history.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=1,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)
        return ""
