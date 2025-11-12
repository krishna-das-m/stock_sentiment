import streamlit as st
import pandas as pd
import plotly.express as px
from newspaper import Article
from newsdataapi import NewsDataApiClient
from datetime import datetime

# from pipeline.data_ingestion_pipeline import DataIngestionPipeline
from config.configuration import ConfigurationManager
from components.data_ingestion import DataIngestion

# Page config
st.set_page_config(
    page_title="Financial News Extractor",
    page_icon="📰",
    layout="wide"
)

# Initialize session state
if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

# Main app
def main():
    st.title("📰 Financial News Extractor")
    st.markdown("Enter a query to extract and analyze financial news articles")
    st.markdown("---")
    
    # Sidebar for input
    with st.sidebar:
        st.header("🔍 Search Parameters")
        
        # Query input
        # Query input with support for multiple queries
        user_query = st.text_area(
            "Enter your search queries (comma-separated):",
            value=st.session_state.last_query,
            placeholder="e.g., HDFC, SBI, ICICI Bank\nor\nNifty 50, Sensex, BSE",
            help="Enter multiple queries separated by commas. Each query will be searched separately."
        )

        # Show parsed queries
        if user_query:
            parsed_queries = [q.strip() for q in user_query.split(',') if q.strip()]
            if len(parsed_queries) > 1:
                st.info(f"📝 Will search for {len(parsed_queries)} queries: {', '.join(parsed_queries)}")
                
        # Number of articles
        num_articles = st.slider(
            "Number of articles to extract:",
            min_value=1,
            max_value=20,
            value=5
        )
        
        # Country selection
        country = st.selectbox(
            "Country:",
            options=['in', 'us', 'gb', 'au'],
            index=0,
            format_func=lambda x: {'in': 'India', 'us': 'USA', 'gb': 'UK', 'au': 'Australia'}[x]
        )
        
        # Extract button
        extract_button = st.button(
            "🚀 Extract News",
            type="primary",
            use_container_width=True
        )
        
        # Example queries with lists
        st.markdown("### 💡 Example Query Sets")
        example_query_sets = {
            'Banking Sector': ['HDFC', 'SBI', 'ICICI Bank', 'Axis Bank'],
            'Market Indices': ['Nifty 50', 'Sensex', 'BSE', 'NSE'],
            'Policy & Economy': ['RBI monetary policy', 'inflation', 'GDP growth'],
            'Tech Stocks': ['TCS', 'Infosys', 'Wipro', 'Tech Mahindra'],
            'Auto Sector': ['Tata Motors', 'Maruti Suzuki', 'Bajaj Auto'],
            'Energy & Oil': ['Reliance', 'ONGC', 'oil prices', 'crude oil']
        }

        for category, queries in example_query_sets.items():
            if st.button(f"{category} ({', '.join(queries[:2])}...)", key=f"example_{category}"):
                # Convert list to string format for the text input
                query_string = ', '.join(queries)
                st.session_state.last_query = query_string
                st.rerun()
    
    # Main content area
    if extract_button and user_query:
        st.session_state.last_query = user_query
        print(user_query)
        
        with st.container():
            st.subheader(f"🔍 Searching for: '{user_query}'")
            
            # Create data ingestion instance
            config_manager = ConfigurationManager()
            data_ingestion = DataIngestion(config_manager)
            
            # Extract articles
            articles = data_ingestion.extract_news(
                query=user_query,
                limit=num_articles,
                country=country
            )
            
            if articles:
                st.session_state.articles = articles
                st.success(f"✅ Extracted {len(articles)} articles successfully!")
                
    # Display results
    if st.session_state.articles:
        st.markdown("---")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Article List", "📊 Quick Stats", "🔍 Detailed View"])
        
        with tab1:
            st.subheader("📋 Extracted Articles")
            
            # Convert to DataFrame for easier handling
            df = pd.DataFrame(st.session_state.articles)
            
            # Show summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📰 Total Articles", len(df))
            with col2:
                unique_sources = df['source'].nunique()
                st.metric("🏢 Unique Sources", unique_sources)
            with col3:
                avg_length = df['full_content'].str.len().mean()
                st.metric("📝 Avg Length", f"{avg_length:.0f} chars")
            with col4:
                latest_date = df['pubDate'].max() if 'pubDate' in df.columns else "N/A"
                st.metric("📅 Latest Article", latest_date)
            
            # Display articles in cards
            for idx, article in enumerate(st.session_state.articles):
                with st.expander(f"📰 {article.get('title', 'Untitled')}"):
                    col_left, col_right = st.columns([3, 1])
                    
                    with col_left:
                        st.write(f"**Description:** {article.get('description', 'No description available')}")
                        
                        # Content preview
                        content = article.get('full_content', '')
                        if content:
                            preview = content[:400] + "..." if len(content) > 400 else content
                            st.write(f"**Content Preview:** {preview}")
                        
                        st.write(f"**Authors:** {article.get('authors', 'Unknown')}")
                    
                    with col_right:
                        st.write(f"**Source:** {article.get('source', 'Unknown')}")
                        st.write(f"**Published:** {article.get('pubDate', 'Unknown')}")
                        st.write(f"**Category:** {article.get('category', 'Business')}")
                        
                        if article.get('url'):
                            st.link_button("🔗 Read Original", article['url'], key=f"link_{idx}")
        
        with tab2:
            st.subheader("📊 Quick Statistics")
            
            if len(st.session_state.articles) > 0:
                df = pd.DataFrame(st.session_state.articles)
                
                # Source distribution
                if 'source' in df.columns:
                    st.write("**Articles by Source:**")
                    source_counts = df['source'].value_counts()
                    st.bar_chart(source_counts)
                
                # Content length distribution
                if 'full_content' in df.columns:
                    st.write("**Content Length Distribution:**")
                    content_lengths = df['full_content'].str.len()
                    st.histogram(content_lengths.dropna(), bins=20)
                
                # Word cloud of titles (if you want to add this)
                st.write("**Common Words in Titles:**")
                all_titles = ' '.join(df['title'].fillna(''))
                words = all_titles.split()
                word_freq = pd.Series(words).value_counts().head(10)
                st.bar_chart(word_freq)
        
        with tab3:
            st.subheader("🔍 Detailed Article View")
            
            if st.session_state.articles:
                # Article selector
                article_options = [f"{i+1}. {article.get('title', 'Untitled')[:60]}..." 
                                for i, article in enumerate(st.session_state.articles)]
                
                selected_idx = st.selectbox(
                    "Choose an article to view in detail:",
                    range(len(article_options)),
                    format_func=lambda x: article_options[x]
                )
                
                if selected_idx is not None:
                    article = st.session_state.articles[selected_idx]
                    
                    # Article header
                    st.markdown(f"## {article.get('title', 'Untitled')}")
                    
                    # Metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Source:** {article.get('source', 'Unknown')}")
                    with col2:
                        st.write(f"**Published:** {article.get('pubDate', 'Unknown')}")
                    with col3:
                        st.write(f"**Authors:** {article.get('authors', 'Unknown')}")
                    
                    # Original link
                    if article.get('url'):
                        st.link_button("🔗 View Original Article", article['url'])
                    
                    st.markdown("---")
                    
                    # Description
                    if article.get('description'):
                        st.write("**Summary:**")
                        st.info(article['description'])
                    
                    # Full content
                    if article.get('full_content'):
                        st.write("**Full Content:**")
                        with st.container():
                            st.markdown(f"<div style='max-height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>{article['full_content']}</div>", 
                                    unsafe_allow_html=True)
                    else:
                        st.warning("Full content not available")
        
        # Download option
        st.markdown("---")
        if st.button("💾 Download Articles as CSV"):
            df = pd.DataFrame(st.session_state.articles)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"news_articles_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()