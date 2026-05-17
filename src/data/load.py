import logging
import pandas as pd
from pathlib import Path
from src.config import ETLConfig

logger = logging.getLogger(__name__)

class DataLoader:
    """Клас для завантаження підготовлених даних у сховище."""

    def __init__(self, config: ETLConfig):
        self.config = config

    def load(self, df: pd.DataFrame) -> Path:
        """
        Зберігає DataFrame у цільову папку в форматі Parquet.
        """
        try:
            # Визначаємо шлях до фінального файлу
            processed_dir = self.config.paths.processed_data_dir
            # Створюємо назву файлу на основі оригінальної, але з розширенням .parquet
            file_name = self.config.source.raw_file_name.replace('.csv', '.parquet')
            output_path = processed_dir / file_name

            logger.info(f"Початок завантаження даних у сховище: {output_path}")

            # Збереження даних (використовуємо engine='pyarrow' або 'fastparquet')
            df.to_parquet(output_path, index=False, engine='pyarrow')

            if output_path.exists():
                logger.info("Дані успішно збережені. Етап Load завершено.")
                return output_path
            else:
                raise IOError("Не вдалося створити файл у цільовій директорії.")

        except Exception as e:
            logger.error(f"Помилка на етапі Load: {e}", exc_info=True)
            raise