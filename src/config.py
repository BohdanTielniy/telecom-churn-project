import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Union
import time


class Config:
    def __init__(self, config_path: Union[str, Path]):
        self.config_path = Path(config_path)
        self._config_data = self._load_yaml()
    
    def _load_yaml(self) -> dict:
        """Метод для зчитування yaml файлу."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Конфігураційний файл не знайдено за шляхом: {self.config_path}")
        except yaml.YAMLError as exc:
            raise Exception(f"Помилка при читанні YAML: {exc}")

class ETLConfig(Config):
    """Клас для управління конфігурацією ETL процесу."""

    @dataclass
    class SourceConfig:
        kaggle_dataset: str
        raw_file_name: str
        metadata_file_name: str

    @dataclass
    class PathsConfig:
        raw_data_dir: Path
        processed_data_dir: Path
        log_file: Path

    @dataclass
    class TransformParams:
        target_column: str
        charges_column: str

    def __init__(self, config_path: Union[str, Path]):
        super().__init__(config_path)
        
        # Ініціалізація підконфігів для зручного доступу
        self.source = self.SourceConfig(**self._config_data['source'])
        raw_file_name = Path(self._config_data['paths']['log_file']['name'])
        log_file_name = raw_file_name if not self._config_data['paths']['log_file']['timestamped_filename'] else Path(raw_file_name.stem + time.strftime("%Y%m%d_%H%M%S") + raw_file_name.suffix)
        self.paths = self.PathsConfig(
            raw_data_dir=Path(self._config_data['paths']['raw_data_dir']),
            processed_data_dir=Path(self._config_data['paths']['processed_data_dir']),
            log_file=Path(self._config_data['paths']['log_file']['dir'] / log_file_name)
        )
        self.transform = self.TransformParams(**self._config_data['transform_params'])

    def create_dirs(self):
        """Метод для автоматичного створення необхідних директорій."""
        self.paths.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.paths.processed_data_dir.mkdir(parents=True, exist_ok=True)
        self.paths.log_file.parent.mkdir(parents=True, exist_ok=True)