import os

import pandas as pd
import tiktoken
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)

embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"
max_tokens = 1500


def get_embedding(text, model="text-embedding-ada-002"):
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def split_into_many(text):
    sentences = text.split('。')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    chunks = []
    tokens_so_far = 0
    chunk = []
    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        if token > max_tokens:
            continue

        chunk.append(sentence)
        tokens_so_far += token + 1

    if chunk:
        chunks.append(". ".join(chunk) + ".")

    return chunks


if __name__ == '__main__':
    df = pd.read_csv("scraped.csv")
    df.columns = ['title', 'text']

    tokenizer = tiktoken.get_encoding(embedding_encoding)
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    shortened = []

    for row in df.iterrows():
        if row[1]['text'] is None:
            continue

        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'])
        else:
            shortened.append(row[1]['text'])

    df = pd.DataFrame(shortened, columns=['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    df["embeddings"] = df.text.apply(lambda x: get_embedding(x, model=embedding_model))
    df.to_csv('embedding.csv')
