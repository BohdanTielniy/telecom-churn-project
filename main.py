import logging
import pandas as pd
from src.config import ProjectConfig
from src.logger import setup_logger
from src.data.extract import DataExtractor
from src.data.transform import DataTransformer
from src.data.load import DataLoader

def main():
    # 1. Ініціалізація конфігурації та логера
    config = ProjectConfig()
    config.create_dirs()
    setup_logger(config.paths.log_file)
    
    logger = logging.getLogger(__name__)
    logger.info("Запуск циклу ETL")

    # EXTRACT
    # Перевіряємо, чи файл вже завантажений, щоб зекономити час та трафік
    raw_path = config.paths.raw_data_dir / config.source.raw_file_name
    if not raw_path.exists():
        extractor = DataExtractor(config)
        raw_path = extractor.extract()
    else:
        logger.info(f"Файл уже знайдено за шляхом {raw_path}. Пропускаємо завантаження.")

    # TRANSFORM
    df_raw = pd.read_csv(raw_path)
    transformer = DataTransformer(config)
    df_processed = transformer.transform(df_raw)

    # LOAD
    loader = DataLoader(config)
    final_path = loader.load(df_processed)

    logger.info(f"ETL-процес завершено успішно. Результат за шляхом: {final_path}")

if __name__ == "__main__":
    main()