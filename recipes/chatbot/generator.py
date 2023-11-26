import os

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def make_content() -> str:
    with open("system.txt", mode="r", encoding="utf-8") as f:
        system = f.read()
    with open("user.txt", mode="r", encoding="utf-8") as f:
        user = f.read()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    return response.choices[0].message.content
