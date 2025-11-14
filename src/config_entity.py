from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    query: list[str] = None

@dataclass(frozen=True)
class SentimentAnalysisConfig:
    model_name: str
    root_dir: Path
    # batch_size: int = 16
    max_length: int = 512
    # device: str = 'cpu'

@dataclass(frozen=True)
class ModelTrainingConfig:
    output_dir: Path
    epochs: int = 3
    learning_rate: float = 2e-5
    train_batch_size: int = 16
    eval_batch_size: int = 16
    warmup_steps: int = 500
    weight_decay: float = 0.01

@dataclass(frozen=True)
class AppConfig:
    title: str
    port: int = 8501
    debug: bool = False
    theme: str = "light"