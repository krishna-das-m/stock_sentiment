# Stock Sentiment Analysis Pipeline

A comprehensive machine learning pipeline for analyzing sentiment in financial news articles using FinBERT and hybrid LLM approaches.


## 🎯 Overview

This project implements an end-to-end sentiment analysis pipeline for financial news, combining:
- **FinBERT** for fast, accurate financial sentiment classification
- **Hybrid LLM Analysis** for detailed explanations and verification
- **ChromaDB** for vector storage and semantic search
- **News APIs** (NewsData.io, MediaStack) for real-time data ingestion


### Prerequisites

- Python 3.8+
- pip or conda or uv
- (Optional) Ollama for local LLM support


## 💻 Usage

### Running Individual Pipelines

**1. Data Ingestion**
```bash
python src/pipeline/data_ingestion_pipeline.py
```

**2. Sentiment Analysis**
```bash
python src/pipeline/sentiment_analysis_pipeline.py
```

**3. Model Training**
```bash
python src/pipeline/model_training_pipeline.py
```

**4. Vector Store**
```bash
python src/pipeline/vector_store_pipeline.py
```


## 🔧 Pipeline Components

### 1. Data Ingestion
- Fetches news from NewsData.io and MediaStack APIs
- Scrapes full article content using newspaper3k
- Saves data in Parquet format
- Supports batch processing and pagination

### 2. Sentiment Analysis
- **FinBERT Analyzer**: Fast sentiment classification (positive/neutral/negative)
- **Hybrid Analyzer**: Combines FinBERT + LLM for detailed explanations
- Returns confidence scores and probability distributions

### 3. Model Training
- Fine-tune FinBERT on custom labeled data
- Supports stratified train/validation splits
- Automatic best model selection
- Comprehensive evaluation metrics

### 4. Vector Store
- Stores articles with embeddings in ChromaDB
- Enables semantic search capabilities
- Filter by sentiment, ticker, date
- Query similar articles



## 🔗 Resources

- [FinBERT Paper](https://arxiv.org/abs/1908.10063)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ for financial sentiment analysis**