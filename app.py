import streamlit as st
import asyncio
import re

from news_agents import get_news


st.set_page_config(
    page_title="Daily News Agent",
    page_icon="📰",
    layout="wide"
)


st.title("📰 Daily News Agent")
st.write("Get the latest news about any topic using AI-powered web research.")


topic = st.text_input(
    "What do you want to know about?",
    placeholder="e.g. Artificial Intelligence, India, Space, Technology"
)


if st.button("🔍 Get Latest News", use_container_width=True):

    if not topic:
        st.warning("Please enter a topic.")

    else:

        with st.spinner("🔎 Searching and summarizing the latest news..."):

            result = asyncio.run(get_news(topic))

        st.success("Latest news found!")

        st.divider()

        # Split articles
        articles = re.split(r"\n\d+\.\s+\*\*Headline:\*\*", result)

        for i, article in enumerate(articles):

            if not article.strip():
                continue

            # Extract headline
            headline_match = re.search(
                r"^(.*?)\n",
                article.strip()
            )

            headline = headline_match.group(1).strip() if headline_match else "News Article"

            # Extract source
            source_match = re.search(
                r"\*\*Source:\*\*\s*(.*)",
                article
            )

            source = source_match.group(1).strip() if source_match else "Unknown"

            # Extract date
            date_match = re.search(
                r"\*\*Publication Date:\*\*\s*(.*)",
                article
            )

            date = date_match.group(1).strip() if date_match else "Date unavailable"

            # Extract summary
            summary_match = re.search(
                r"\*\*Short Summary:\*\*\s*(.*)",
                article
            )

            summary = summary_match.group(1).strip() if summary_match else ""

            # Extract URL
            url_match = re.search(
                r"\[https?://[^\]]+\]\((https?://[^)]+)\)",
                article
            )

            url = url_match.group(1) if url_match else ""

            # News card
            with st.container(border=True):

                st.subheader(f"📰 {headline}")

                col1, col2 = st.columns(2)

                with col1:
                    st.caption(f"🗞️ **Source:** {source}")

                with col2:
                    st.caption(f"📅 **Published:** {date}")

                st.write(summary)

                if url:
                    st.link_button(
                        "Read Full Article →",
                        url
                    )