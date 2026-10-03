# 📊 Daily News Agent - Workflow & Architecture Specification

This document provides a detailed breakdown of the internal workflow, data transformations, and component interactions within the **Daily News Agent** application.

---

## 🏗️ High-Level System Architecture

```mermaid
flowchart TD
    subgraph Frontend ["📱 User Interface Layer (app.py)"]
        UI_INPUT[👤 User Input: News Topic]
        UI_SPINNER[🔎 Loading Spinner State]
        UI_REGEX[⚡ Regex Output Parser]
        UI_DISPLAY[📺 Streamlit Custom News Cards]
    end

    subgraph Orchestrator ["🤖 Agent Orchestration Layer (news_agents.py)"]
        FUNC[⚡ get_news Async Handler]
        CREW[👥 CrewAI Framework Controller]
        AGENT[🕵️ News Researcher Agent]
        TASK[📋 Research Task Engine]
    end

    subgraph ExternalServices ["🌐 External APIs & LLM"]
        SERPER[🌐 Serper Web Search API]
        GEMINI[🧠 Google Gemini 3.5 Flash Lite LLM]
    end

    UI_INPUT -->|Click 'Get Latest News'| UI_SPINNER
    UI_SPINNER -->|asyncio.run| FUNC
    FUNC --> CREW
    CREW --> TASK
    TASK --> AGENT
    AGENT -->|1. Web Search Query| SERPER
    SERPER -->|2. Search Results JSON| AGENT
    AGENT -->|3. Prompt + Search Context| GEMINI
    GEMINI -->|4. AI Structured Summaries| AGENT
    AGENT -->|5. Raw Output String| FUNC
    FUNC --> UI_REGEX
    UI_REGEX --> UI_DISPLAY
```

---

## ⏱️ End-to-End Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant UI as 📱 Streamlit App (app.py)
    participant Function as ⚡ get_news() Handler
    participant Crew as 🤖 CrewAI Engine (news_agents.py)
    participant Serper as 🌐 Serper Search API
    participant Gemini as 🧠 Google Gemini LLM

    User->>UI: Enters news topic (e.g., "Saudi Arabia") & clicks "Get Latest News"
    UI->>Function: Invokes asyncio.run(get_news(topic))
    Function->>Crew: Triggers news_crew.kickoff_async(inputs={"topic": topic})
    Crew->>Serper: News Researcher Agent calls SerperDevTool with search query
    Serper-->>Crew: Returns live Google search snippets & links
    Crew->>Gemini: Passes search context + prompt guidelines to LLM
    Gemini-->>Crew: Generates top 3 news articles (Headline, Source, Date, Summary, URL)
    Crew-->>Function: Returns result string
    Function-->>UI: Passes result text to Streamlit UI
    UI->>UI: Parses raw text using Regex into structured data objects
    UI-->>User: Renders interactive news cards with source badges & article links
```

---

## 🔄 Detailed Step-by-Step Data Flow

| Step | Component | Action | Description |
| :--- | :--- | :--- | :--- |
| **1** | **Streamlit UI** (`app.py`) | User Input | Captures the search topic entered by the user. |
| **2** | **Async Event Loop** | Trigger Execution | Runs `asyncio.run(get_news(topic))` to trigger non-blocking backend execution. |
| **3** | **CrewAI Engine** (`news_agents.py`) | Task Kickoff | Passes topic input to `news_crew.kickoff_async()` containing the `News Researcher` agent. |
| **4** | **SerperDevTool** | Web Retrieval | Queries Google Search API for recent articles from the past few days. |
| **5** | **Google Gemini LLM** | Context Processing | Evaluates search snippets, selects 3 key articles, extracts metadata (Headline, Source, Date, Summary, URL). |
| **6** | **Regex Parser** (`app.py`) | Data Structuring | Uses Regular Expressions (`re.split` & `re.search`) to isolate individual article fields. |
| **7** | **Streamlit Container** | UI Rendering | Displays styled news cards with source badges, publication dates, and `Read Full Article →` links. |

---

## 👤 Author

- **dhanshreeg03** - [GitHub Repository](https://github.com/dhanshreeg03/Dailynewsagent)
