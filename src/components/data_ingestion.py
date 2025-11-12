import pandas as pd
import os
import pickle

from dataclasses import dataclass
from pathlib import Path
from newspaper import Article
from newsdataapi import NewsDataApiClient

from config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config
        self.all_news_articles = None
    
    def newsdata_connect(self):
        try:
            api = NewsDataApiClient(apikey='pub_965468a202be412d80928d294b632639')
            print('connected to API')
            return api
        except Exception as e:
            print("Not connected to API")
            return None
        

    def extract_news(self, query:list[str], limit:int=5, country:str='in'):
        api = self.newsdata_connect()
        search_query = query or (self.config.query if self.config.query else 'finance')
        # Combine queries into a single OR-separated string with quotes
        combined_query = " OR ".join([f'"{q}"' for q in search_query])
        print(combined_query)
        try:
            response = api.latest_api(
                q=combined_query,
                country=country,
                category='business',
                size=limit,
                language='en'
            )
            articles = response.get('results',[])
            print(articles)
        except Exception as e:
            print("No articles returned")
            return []

        # step 2: scrape full content from each URL
        full_articles = []
        for idx, article in enumerate(articles, 1):
            try:
                print(f"Processing {idx}/{len(articles)}: {article['title'][:50]}...")
                url = article.get('link') # article['link']
                if not url:
                    print("Skipping: No url")
                    continue
                # get full content
                news_article = Article(url)
                news_article.download()
                news_article.parse()
                full_articles.append({
                    'article_id': article['article_id'],
                    'title': article['title'],
                    'description': article['description'],
                    'source': article['source_name'],
                    'url': article['link'],
                    'pubDate': article['pubDate'],
                    'category': article['category'],
                    'full_content': news_article.text,
                    'authors': ', '.join(news_article.authors),
                    'image_url': article['image_url']
                })
            except Exception as e:
                print(f"Error scraping {article['link']}: {e}")
        self.all_news_articles = full_articles
        return self.all_news_articles

    def save_newsdata(self):
        filepath = os.path.join(self.config.root_dir, 'news_articles.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(self.all_news_articles, f)
    
    def load_newsdata(self):
        filepath = os.path.join(self.config.root_dir, 'news_articles.pkl')
        with open(filepath, 'rb') as f:
            self.news_articles = pickle.load(f)
        return self.news_articles