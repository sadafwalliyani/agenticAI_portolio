import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import ArxivAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from dotenv import load_dotenv
import os
from utils_research_sum_app import getAgent  # assuming getAgent is defined elsewhere
from textblob import TextBlob
def main():
# Load environment variables
    load_dotenv()

# Ensure the API key is loaded
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.0,
    google_api_key=GOOGLE_API_KEY,
)

# Tools Initialization
arxiv_tool = ArxivAPIWrapper()

# Sentiment analysis tool
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return f"Sentiment polarity: {analysis.sentiment.polarity}, Sentiment subjectivity: {analysis.sentiment.subjectivity}"

# Research highlights extraction
def extract_highlights(text):
    highlights = text.split(".")[:5]  # Extract first 5 sentences as highlights
    return " | ".join(highlights)

# Full-text search
def search_text(text, query):
    results = [line for line in text.splitlines() if query.lower() in line.lower()]
    if not results:
        return "No results found for your query."
    return " | ".join(results)

# Tools List (Removed Paper Downloader)
tools = [
    Tool(
        name="Research Summarizer",
        func=arxiv_tool.run,
        description="Summarize research papers using Arxiv API.",
    ),
    Tool(
        name="Sentiment Analyzer",
        func=analyze_sentiment,
        description="Analyze the sentiment of the research paper.",
    ),
    Tool(
        name="Research Highlights",
        func=extract_highlights,
        description="Extract key points and highlights from research papers.",
    ),
    Tool(
        name="Full-Text Search",
        func=search_text,
        description="Search for specific terms within the text of a research paper.",
    ),
]

# Pull Prompt from LangChain Hub
try:
    prompt = hub.pull("hwchase17/react")
except Exception as e:
    raise RuntimeError(f"Failed to pull prompt from LangChain Hub: {e}")

# Define Agent
def getAgent():
    try:
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor
    except Exception as e:
        raise RuntimeError(f"Failed to create agent: {e}")

# Streamlit UI Setup
st.title("arXiv Research Paper Summarizer Agent")
st.write("Summarize, analyze, and search research papers using various tools.")

# Paper number input
paper_number = st.text_input("Enter the paper number", "")

if paper_number:
    # Get the agent executor
    agent_executor = getAgent()

    # Run the Research Summarizer tool
    if st.button("Summarize Research Paper"):
        try:
            response = arxiv_tool.run(paper_number)  # Directly use paper_number
            if not response or response.strip() == "":
                st.error("The paper content could not be retrieved. Please check the paper number.")
            else:
                st.write("### Summary")
                st.write(response)
        except Exception as e:
            st.error(f"Error fetching paper: {e}")

    # Sentiment Analysis
    if st.button("Analyze Sentiment"):
        try:
            paper_text = arxiv_tool.run(paper_number)  # Directly use paper_number
            if not paper_text or paper_text.strip() == "":
                st.error("The paper content could not be retrieved. Please check the paper number.")
            else:
                sentiment_result = analyze_sentiment(paper_text)
                st.write("### Sentiment Analysis")
                st.write(sentiment_result)
        except Exception as e:
            st.error(f"Error analyzing sentiment: {e}")

    # Research Highlights Extraction
    if st.button("Extract Highlights"):
        try:
            paper_text = arxiv_tool.run(paper_number)
            if not paper_text or paper_text.strip() == "":
                st.error("The paper content could not be retrieved. Please check the paper number.")
            else:
                highlights = extract_highlights(paper_text)
                st.write("### Research Highlights")
                st.write(highlights)
        except Exception as e:
            st.error(f"Error extracting highlights: {e}")

    # Full-Text Search with Validation
    search_query = st.text_input("Enter search query within the paper", "")
    if search_query and st.button("Search Text in Paper"):
        try:
            paper_text = arxiv_tool.run(paper_number)
            if not paper_text or paper_text.strip() == "":
                st.error("The paper content could not be retrieved. Please check the paper number.")
            else:
                search_results = search_text(paper_text, search_query)  # Replace with search_text_fuzzy for fuzzy search
                st.write("### Search Results")
                st.write(search_results)
        except Exception as e:
            st.error(f"Error searching in paper: {e}")

if __name__ == "__main__":
    main()
    