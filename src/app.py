import streamlit as st
import pandas as pd
import plotly.express as px
from newspaper import Article
from newsdataapi import NewsDataApiClient
from datetime import datetime

from config.configuration import ConfigurationManager
from components.data_ingestion import DataIngestion

from pages import sentiment, news_extractor

# Page config
st.set_page_config(
    page_title="Financial Sentiment Analysis",
    page_icon="📰",
    layout="wide"
)

# Initialize session state - FIX: Add missing query_display and fix last_query type
if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'last_query' not in st.session_state:
    st.session_state.last_query = []  # Changed from "" to []
if 'query_display' not in st.session_state:
    st.session_state.query_display = ""  # Added missing initialization
# Initialize session state
if 'sentiment_results' not in st.session_state:
    st.session_state.sentiment_results = []

def main():
    st.title("📰 Financial News Sentiment")
    st.markdown("A screener for stocks based on sentiment analysis of financial news")
    st.markdown("---")
    
        
    # Sidebar for input
    with st.sidebar:
        st.header('Navigation')
        
        # Navigation buttons
        views = {
            'Sentiment Analysis': sentiment,
            'News Extractor': news_extractor,
            # 'Currency Markets': currency_markets,
            # 'Crypto Markets': crypto_markets
        }
        for view_name, view_module in views.items():
            if st.button(view_name, key=view_name, help=None, use_container_width=True):
                st.session_state.current_view = view_name
    
    # Main content area
    # Display content based on selected view
    current_view = st.session_state.current_view
    if current_view in views:
        views[current_view].show()


if __name__ == "__main__":
    main()