from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import ArxivAPIWrapper
from dotenv import load_dotenv
import os
import requests
from textblob import TextBlob

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

# Arxiv summarization tool
arxiv_tool = ArxivAPIWrapper()

# Sentiment analysis tool
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return f"Sentiment polarity: {analysis.sentiment.polarity}, Sentiment subjectivity: {analysis.sentiment.subjectivity}"

# Research highlights extraction
def extract_highlights(text):
    highlights = text.split(".")[:5]
    return " | ".join(highlights)

# Full-text search tool
def search_text(text, query):
    return [line for line in text.splitlines() if query.lower() in line.lower()]

# Paper downloader tool
def download_paper(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Failed to download the paper: {e}"

# Define AgentExecutor
def getAgent():
    """Creates and returns the AgentExecutor."""
    try:
        agent = create_react_agent(llm, [arxiv_tool, analyze_sentiment, extract_highlights, search_text, download_paper], None)
        agent_executor = AgentExecutor(agent=agent, tools=[arxiv_tool, analyze_sentiment, extract_highlights, search_text, download_paper], verbose=True)
        return agent_executor
    except Exception as e:
        raise RuntimeError(f"Failed to create agent: {e}")
