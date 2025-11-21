import mysql.connector
from mysql.connector import Error, pooling
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging
from pathlib import Path

from config_entity import DatabaseConfig
logger = logging.getLogger(__name__)
class Database:
    def __init__(self, config=DatabaseConfig):
        self.config = config
        self.connection_pool = None
        
        if config.enabled:
            self._create_connection_pool()

    def _create_connection_pool(self):
        self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="finews_pool",
            pool_size=self.config.pool_size,
            pool_reset_session=True,
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            charset=self.config.charset
        )
        logger.info("MySQL connection pool created")

    def get_connection(self):
        if not self.config.enabled or not self.connection_pool:
            return None
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection: {e}")
            return None
        
    # ========== Article Operations ========== #

    def insert_articles_batch(self, articles:List[Dict]) ->bool:
        if not self.config.enabled:
            return (0, len(articles))
        
        connection = self.get_connection()
        if not connection:
            return (0, len(articles))
        
        successful = 0
        failed = 0

        cursor = connection.cursor()
        query = """
                INSERT INTO news_articles 
                (article_id, title, description, content, source, published_date,
                url, category, country, language)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        for article in articles:
                try:
                    data = (
                        article.get('article_id'),
                        article.get('title'),
                        article.get('description', ''),
                        article.get('content', ''),
                        article.get('source', 'Unknown'),
                        article.get('published_date'),
                        article.get('url', ''),
                        article.get('category', 'business'),
                        article.get('country', 'IN'),
                        article.get('language', 'en')
                    )
                    cursor.execute(query, data)
                    successful += 1
                except mysql.connector.IntegrityError:
                    failed += 1
        connection.commit()
        logger.info(f"Batch insert: {successful} success, {failed} failed")
        cursor.close()
        connection.close()  

    # ========== SENTIMENT OPERATIONS ==========
    
    def insert_sentiment(self, sentiment: Dict) -> bool:
        """Insert sentiment analysis result"""
        if not self.config.enabled:
            return False
            
        connection = self.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            query = """
                INSERT INTO sentiment_analysis
                (article_id, model_name, sentiment, confidence,
                positive_score, negative_score, neutral_score,
                processing_time_ms)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                sentiment = VALUES(sentiment),
                confidence = VALUES(confidence),
                positive_score = VALUES(positive_score),
                negative_score = VALUES(negative_score),
                neutral_score = VALUES(neutral_score),
                processing_time_ms = VALUES(processing_time_ms)
            """
            
            data = (
                sentiment.get('article_id'),
                sentiment.get('model_name'),
                sentiment.get('sentiment'),
                sentiment.get('confidence'),
                sentiment.get('positive_score', 0.0),
                sentiment.get('negative_score', 0.0),
                sentiment.get('neutral_score', 0.0),
                sentiment.get('processing_time_ms', 0.0)
            )
            
            cursor.execute(query, data)
            connection.commit()
            return True
            
        except Error as e:
            logger.error(f"Insert sentiment error: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()