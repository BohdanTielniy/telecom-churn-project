import logging
import json
from datetime import datetime
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from src.config import ProjectConfig

logger = logging.getLogger(__name__)

class DataExtractor:
    """Клас для завантаження даних з Kaggle."""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.api = KaggleApi()
        try:
            self.api.authenticate()
        except Exception as e:
            logger.error(f"Помилка авторизації Kaggle API: {e}")
            raise

    def extract(self) -> Path:
        """
        Завантажує датасет, фіксує час у метаданих та зберігає у raw директорію.
        """
        dataset = self.config.source.kaggle_dataset
        raw_dir = self.config.paths.raw_data_dir
        
        logger.info(f"Початок завантаження датасету: {dataset}")

        try:
            self.api.dataset_download_files(
                dataset, 
                path=raw_dir, 
                unzip=True
            )
            
            raw_file_path = raw_dir / self.config.source.raw_file_name
            metadata_path = raw_dir / self.config.source.metadata_file_name
            extraction_time = datetime.now().isoformat()
            metadata = {
                    "source": dataset,
                    "extraction_time": extraction_time,
                    "file_saved_at": str(raw_file_path),
                }
            
            if raw_file_path.exists():
                metadata["status"] = "Success"
                with open(metadata_path, "w", encoding="utf-8") as meta_file:
                    json.dump(metadata, meta_file, indent=4)
                
                logger.info(f"Дані успішно завантажені. Метадані зафіксовано у {metadata_path}")
                return raw_file_path
            else:
                metadata["status"] = "Failed"
                with open(metadata_path, "w", encoding="utf-8") as meta_file:
                    json.dump(metadata, meta_file, indent=4)
                raise FileNotFoundError(f"Файл {self.config.source.raw_file_name} не знайдено.")


        except Exception as e:
            logger.error(f"Критична помилка під час етапу Extract: {e}", exc_info=True)
            raise
