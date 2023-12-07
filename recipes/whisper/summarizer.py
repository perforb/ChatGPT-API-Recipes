import os

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)

if __name__ == '__main__':
    with open("sample.wav", "rb") as file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file
        )

    summary = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"以下の文章を3行の箇条書きで要約してください:\n{transcript.text}"
            },
        ],
    )

    print(summary.choices[0].message.content)
