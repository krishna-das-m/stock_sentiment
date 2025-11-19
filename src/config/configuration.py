from constants import *
from config_entity import DataIngestionConfig, SentimentAnalysisConfig, DatabaseConfig
from utils.common import read_yaml, create_directories

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH,
                        ):
        self.config = read_yaml(config_filepath)

    def get_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            query= config.query
        )
        return data_ingestion_config
    
    def get_sentiment_analysis_config(self):
        config = self.config.sentiment_analysis
        sentiment_analysis_config = SentimentAnalysisConfig(
            model_name= config.model_name,
            max_length= config.max_length,
            root_dir=config.root_dir
        )
        return sentiment_analysis_config
    
    def get_database_config(self):
        config = self.config.database
        database_config = DatabaseConfig(
            enabled=config.enabled,
            type=config.type,
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.password,
            pool_size=config.get('pool_size', 10),
            charset=config.get('charset', 'utf8mb4')
        )
        return database_config