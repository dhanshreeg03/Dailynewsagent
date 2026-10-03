import asyncio
from news_agents import get_news


async def main():

    topic = input("Enter a news topic: ")

    result = await get_news(topic)

    print("\n===== LATEST NEWS =====\n")
    print(result)


asyncio.run(main())