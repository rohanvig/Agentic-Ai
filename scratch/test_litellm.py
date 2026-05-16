import litellm
import os
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True)

async def test():
    print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')[:10]}...")
    try:
        response = await litellm.acompletion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": "hi"}],
            api_key=os.getenv("GEMINI_API_KEY")
        )
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
