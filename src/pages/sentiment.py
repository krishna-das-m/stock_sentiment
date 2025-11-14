import streamlit as st
from components.sentiment_analysis import FinBERTSentimentAnalyzer, HybridFinancialAnalyzer
from components.data_ingestion import DataIngestion
from config.configuration import ConfigurationManager

def show():
    st.header("Sentiment Analysis")
    st.markdown("Analyze sentiment of financial news articles using FinBERT and LLM")
    st.markdown("---")

    # # Initialize session state
    # if 'sentiment_results' not in st.session_state:
    #     st.session_state.sentiment_results = []
    # if 'articles' not in st.session_state:
    #     st.session_state.articles = []

    use_llm = st.selectbox(
        "Use LLM for detailed analysis",
        value=False,
        help="slower but provide detailed explanation"
    )

    analysis_source = st.radio(
            "Select data source:",
            ["Use extracted articles", "Enter custom text", "Load from file"]
        )