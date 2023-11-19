import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI

_ = load_dotenv(find_dotenv())

client = AsyncOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)


async def main() -> None:
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Say this is a test"
            },
        ],
    )

    message = completion.choices[0].message.content
    print(message)


asyncio.run(main())
