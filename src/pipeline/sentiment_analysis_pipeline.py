# import sys
# from pathlib import Path

# src_path = Path(__file__).parent.parent
# sys.path.append(str(src_path))


from config.configuration import ConfigurationManager
from components.sentiment_analysis import FinBERTSentimentAnalyzer, HybridFinancialAnalyzer
import pickle

class SentimentAnalysisPipeline:
    def __init__(self):
        pass

    def main(self):
        with open('artifacts/data_ingestion/news_articles.pkl', 'rb') as f:
            news_articles = pickle.load(f)
        # news = news_articles['full_content']
        config = ConfigurationManager()
        sentiment_analysis_config = config.get_sentiment_analysis_config()
        FinBERTanalyzer = FinBERTSentimentAnalyzer(config=sentiment_analysis_config)
        # Hybridanalyzer = HybridFinancialAnalyzer(config=sentiment_analysis_config)
        FinBERTanalyzer.batch_analyze(news_articles)
        FinBERTanalyzer.save_sentiment_data()
        # Hybridanalyzer.batch_analyze(news_articles)
        # Hybridanalyzer.save_sentiment_data()

if __name__ =="__main__":
    try:
        obj = SentimentAnalysisPipeline()
        obj.main()
    except Exception as e:
        raise e