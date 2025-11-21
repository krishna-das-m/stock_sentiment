import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

from config.configuration import ConfigurationManager
from components.data_ingestion import DataIngestion
from components.database import Database
import logging
logger = logging.getLogger(__name__)

STAGE_NAME = "Data Ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        data_ingestion_config = config_manager.get_data_ingestion_config()
        db_config = config_manager.get_database_config()

        data_ingestion = DataIngestion(config=data_ingestion_config)
        articles = data_ingestion.extract_news()
        data_ingestion.save_newsdata()

        # store in database
        db = Database(config=db_config)
        success, failed = db.insert_articles_batch(articles)
        logger.info(f"Stored {success} new articles, {failed} duplicates")
        logger.info(">>> News Collection Complete <<<")
            
        return success
    
if __name__ == '__main__':
    try:
        obj = DataIngestionPipeline()
        obj.main()
    except Exception as e:
        raise e