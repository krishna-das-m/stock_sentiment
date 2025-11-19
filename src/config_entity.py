from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

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

@dataclass(frozen=True)
class DatabaseConfig:
    enabled: bool
    type: str
    host: str
    port: int
    database: str
    user: str
    password: str
    pool_size: int = 10
    charset: str = "utf8mb4"

    def __post_init__(self):
        # Replace ${ENV_VAR} with actual value
        if self.password.startswith("${") and self.password.endswith("}"):
            env_var = self.password[2:-1]
            actual_password = os.getenv(env_var)
            if actual_password:
                object.__setattr__(self, 'password', actual_password)
            else:
                raise ValueError(
                    f"Environment variable '{env_var}' not found. "
                    f"Make sure it's defined in your .env file."
                )
        elif not self.password:
            raise ValueError("Database password is required but was not provided")
