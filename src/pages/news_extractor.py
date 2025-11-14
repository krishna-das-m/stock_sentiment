import streamlit as st
import pandas as pd
from datetime import datetime

from config.configuration import ConfigurationManager
from components.data_ingestion import DataIngestion

def show():
    st.header("Financial News Extractor")

    st.header("🔍 Search Parameters")
        
    # Query input with support for multiple queries
    user_query = st.text_area(
        "Enter your search queries (comma-separated):",
        value=st.session_state.query_display,
        placeholder="e.g., HDFC, SBI, ICICI Bank\nor\nNifty 50, Sensex, BSE",
        help="Enter multiple queries separated by commas. Each query will be searched separately."
    )

    # Parse and update session state when user types
    if user_query != st.session_state.query_display:
        # User has typed something new
        parsed_queries = [q.strip() for q in user_query.split(',') if q.strip()]
        st.session_state.last_query = parsed_queries
        st.session_state.query_display = user_query

    # Show parsed queries
    if st.session_state.last_query:
        if len(st.session_state.last_query) > 1:
            st.info(f"📝 Will search for {len(st.session_state.last_query)} queries: {', '.join(st.session_state.last_query)}")
        else:
            st.info(f"📝 Will search for: {st.session_state.last_query[0]}")

    # FIX: Move num_articles outside the if block and fix indentation
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
            # Keep as list in session state
            st.session_state.last_query = queries
            st.session_state.query_display = ', '.join(queries)
            st.rerun()
    
    # Main content area
        
    if extract_button and st.session_state.last_query:
        query_list = st.session_state.last_query  # This is already a list
        
        with st.container():
            if len(query_list) == 1:
                st.subheader(f"🔍 Searching for: '{query_list[0]}'")
            else:
                st.subheader(f"🔍 Searching for {len(query_list)} queries:")
                for i, q in enumerate(query_list, 1):
                    st.write(f"  {i}. **{q}**")
            
            # Create data ingestion instance
            try:
                config_manager = ConfigurationManager()
                data_ingestion = DataIngestion(config_manager)
                
                # Extract articles - pass the list directly
                articles = data_ingestion.extract_news(
                    query=query_list,  # Pass as list
                    limit=num_articles,
                    country=country
                )
                
                if articles:
                    st.session_state.articles = articles
                    
                    # Show breakdown by query if multiple queries
                    if len(query_list) > 1:
                        df = pd.DataFrame(articles)
                        if 'search_query' in df.columns:
                            query_breakdown = df['search_query'].value_counts()
                            st.success(f"✅ Extracted {len(articles)} articles successfully!")
                            
                            with st.expander("📊 Results breakdown by query"):
                                for query, count in query_breakdown.items():
                                    st.write(f"• **{query}**: {count} articles")
                    else:
                        st.success(f"✅ Extracted {len(articles)} articles successfully!")
                else:
                    st.warning("No articles found for the given queries.")
                    
            except Exception as e:
                st.error(f"Error during extraction: {str(e)}")
                
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
                unique_sources = df['source'].nunique() if 'source' in df.columns else 0
                st.metric("🏢 Unique Sources", unique_sources)
            with col3:
                if 'full_content' in df.columns and not df['full_content'].isna().all():
                    avg_length = df['full_content'].str.len().mean()
                    st.metric("📝 Avg Length", f"{avg_length:.0f} chars")
                else:
                    st.metric("📝 Avg Length", "N/A")
            with col4:
                latest_date = df['pubDate'].max() if 'pubDate' in df.columns else "N/A"
                st.metric("📅 Latest Article", latest_date)
            
            # Display articles in cards
            for idx, article in enumerate(st.session_state.articles):
                with st.expander(f"📰 {article.get('title', 'Untitled')}"):
                    # Add query tag if available
                    if article.get('search_query'):
                        st.markdown(f"🔍 **Found via query:** `{article['search_query']}`")
                    
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
                            st.link_button("🔗 Read Original", article['url'])
        
        # Rest of your tabs code...
        with tab2:
            st.subheader("📊 Quick Statistics")
            
            if len(st.session_state.articles) > 0:
                df = pd.DataFrame(st.session_state.articles)
                
                # Query-wise distribution if multiple queries
                if 'search_query' in df.columns:
                    st.write("**Articles by Search Query:**")
                    query_counts = df['search_query'].value_counts()
                    st.bar_chart(query_counts)
                
                # Source distribution
                if 'source' in df.columns:
                    st.write("**Articles by Source:**")
                    source_counts = df['source'].value_counts()
                    st.bar_chart(source_counts)
                
                # Content length distribution
                if 'full_content' in df.columns:
                    content_lengths = df['full_content'].str.len().dropna()
                    if not content_lengths.empty:
                        st.write("**Content Length Distribution:**")
                        st.bar_chart(content_lengths)
                
                # Word frequency in titles
                st.write("**Common Words in Titles:**")
                all_titles = ' '.join(df['title'].fillna(''))
                words = [word.lower() for word in all_titles.split() if len(word) > 3]
                if words:
                    word_freq = pd.Series(words).value_counts().head(10)
                    st.bar_chart(word_freq)
        
        with tab3:
            # Your existing tab3 code...
            st.subheader("🔍 Detailed Article View")
            
            if st.session_state.articles:
                article_options = [f"{i+1}. {article.get('title', 'Untitled')[:60]}..." 
                                for i, article in enumerate(st.session_state.articles)]
                
                selected_idx = st.selectbox(
                    "Choose an article to view in detail:",
                    range(len(article_options)),
                    format_func=lambda x: article_options[x]
                )
                
                if selected_idx is not None:
                    article = st.session_state.articles[selected_idx]
                    
                    st.markdown(f"## {article.get('title', 'Untitled')}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Source:** {article.get('source', 'Unknown')}")
                    with col2:
                        st.write(f"**Published:** {article.get('pubDate', 'Unknown')}")
                    with col3:
                        st.write(f"**Authors:** {article.get('authors', 'Unknown')}")
                    
                    if article.get('url'):
                        st.link_button("🔗 View Original Article", article['url'])
                    
                    st.markdown("---")
                    
                    if article.get('description'):
                        st.write("**Summary:**")
                        st.info(article['description'])
                    
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
