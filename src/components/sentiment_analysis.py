import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Union
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

from config_entity import SentimentAnalysisConfig
import os
import pickle
import time
# from utils.logger import logger

class FinBERTSentimentAnalyzer:
    def __init__(self, config: SentimentAnalysisConfig = None):
        """Initialize FinBERT model"""
        self.config = config
        model_name = config.model_name if config else "ProsusAI/finbert"
        
        # logger.info(f"Loading FinBERT model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.labels = ["positive", "negative", "neutral"]
        self.sentiment_data = None
        # logger.info("FinBERT model loaded successfully")
    
    def analyze(self, news_text: str) -> Dict[str, any]:
        """Analyze sentiment with probabilities"""
        max_length = self.config.max_length if self.config else 512
        
        inputs = self.tokenizer(
            news_text, 
            return_tensors="pt",
            truncation=True, 
            max_length=max_length
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        scores = predictions[0].tolist()
        sentiment_dict = {label: score for label, score in zip(self.labels, scores)}
        
        # Get primary sentiment
        primary_sentiment = self.labels[scores.index(max(scores))]
        confidence = max(scores)
        
        return {
            "sentiment": primary_sentiment,
            "confidence": confidence,
            "scores": sentiment_dict,
            "text": news_text
        }
    
    def batch_analyze(self, news_list: List[str]) -> List[Dict]:
        """Analyze multiple news items"""
        self.sentiment_data = [self.analyze(news['full_content']) for news in news_list]
    
    def save_sentiment_data(self):
        filepath = os.path.join(self.config.root_dir, 'news_sentiment.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(self.sentiment_data, f)

class HybridFinancialAnalyzer:
    def __init__(self, config: SentimentAnalysisConfig = None):
        self.config = config
        self.finbert = FinBERTSentimentAnalyzer(config)
        self.llm = OllamaLLM(model="minimax-m2:cloud", temperature=0.1)
        
        self.llm_sentiment_data = None
        self.explanation_prompt = PromptTemplate(
            input_variables=["news_text", "sentiment", "confidence"],
            template="""The following financial news has been classified as {sentiment} with {confidence:.1%} confidence:

            News: {news_text}

            Provide a detailed analysis explaining:
            1. Why this sentiment classification makes sense
            2. Key financial indicators or events mentioned
            3. Potential market implications
            4. Any risks or uncertainties

            Analysis:"""
                    )

    def analyze(self, news_text: str) -> Dict:
        """Perform hybrid analysis combining FinBERT and LLM"""
        # logger.info("Analyzing sentiment with FinBERT...")
        finbert_result = self.finbert.analyze(news_text)

        # logger.info("Generating detailed analysis with LLM...")
        chain = self.explanation_prompt | self.llm
        
        explanation = chain.invoke({
            "news_text": news_text,
            "sentiment": finbert_result['sentiment'],
            "confidence": finbert_result['confidence']
        })
        
        # logger.info("Analysis complete")
        return {
            **finbert_result,
            "detailed_analysis": explanation
        }
    
    def batch_analyze(self, news_list: List[str]) -> List[Dict]:
        """Analyze multiple news items"""
        start = time.time()
        self.llm_sentiment_data = [self.analyze(news['full_content']) for news in news_list]
        end = time.time()
        print(f"Time elapsed: {end-start} s")

    def save_sentiment_data(self):
        filepath = os.path.join(self.config.root_dir, 'news_llm_sentiment.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(self.llm_sentiment_data, f)