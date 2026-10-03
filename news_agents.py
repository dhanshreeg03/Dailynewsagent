from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

load_dotenv()


# Gemini LLM
llm = LLM(
    model="gemini/gemini-3.5-flash-lite"
)


# Serper web search
search_tool = SerperDevTool()


# News Researcher
news_researcher = Agent(
    role="News Researcher",

    goal="Find the latest news about the user's topic using web search.",

    backstory="""
    You are a careful news researcher.
    You MUST use the web search tool to find current information.
    Never rely only on your existing knowledge.
    """,

    tools=[search_tool],
    llm=llm,
    verbose=True
)


# Research Task
research_task = Task(
    description="""
    Find the latest news about {topic}.

    IMPORTANT:
    - Use the web search tool.
    - Search for news from the last few days.
    - Find 3 relevant articles.
    - Do not answer from existing knowledge.

    For each article provide:
    - Headline
    - Source
    - Publication date
    - Short summary
    - URL
    """,

    expected_output="""
    A list of 3 recent news articles with:
    headline, source, publication date,
    short summary, and URL.
    """,

    agent=news_researcher
)


# Crew
news_crew = Crew(
    agents=[news_researcher],
    tasks=[research_task],
    verbose=True
)


# Function that our frontend will call
async def get_news(topic):

    result = await news_crew.kickoff_async(
        inputs={"topic": topic}
    )

    return result.raw