from pathlib import Path
import os

PROJECT_ROOT = Path(os.getcwd()).parent
CONFIG_FILE_PATH = Path(PROJECT_ROOT/"config/config.yaml")
PARAMS_FILE_PATH = PROJECT_ROOT / "params.yaml"

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = DATA_DIR / "artifacts"

# Model paths
MODELS_DIR = PROJECT_ROOT / "models"
FINBERT_MODEL_DIR = MODELS_DIR / "finbert"
TRAINED_MODELS_DIR = MODELS_DIR / "trained_models"

# API Configuration
DEFAULT_NEWS_SOURCES = ["newsapi", "mediastack", "newsdata"]
DEFAULT_CATEGORIES = ["business", "technology", "finance"]
DEFAULT_COUNTRIES = ["in", "us"]

# Model Configuration
FINBERT_MODEL_NAME = "ProsusAI/finbert"
MAX_SEQUENCE_LENGTH = 512
SENTIMENT_LABELS = ["positive", "negative", "neutral"]