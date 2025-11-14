import sys
from pathlib import Path

src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

from config.configuration import ConfigurationManager
from components.data_ingestion import DataIngestion


STAGE_NAME = "Data Ingestion stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        data_ingestion_config = config_manager.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.extract_news()
        data_ingestion.save_newsdata()


    
if __name__ == '__main__':
    try:
        obj = DataIngestionPipeline()
        obj.main()
    except Exception as e:
        raise e