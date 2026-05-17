import pandas as pd
import numpy as np
import logging
from src.config import ETLConfig

logger = logging.getLogger(__name__)

class DataTransformer:
    """Клас для очищення та перетворення даних телеком-компанії."""

    def __init__(self, config: ETLConfig):
        self.config = config

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Основний метод трансформації даних.
        """
        try:
            logger.info("Початок етапу Transform...")
            
            # Копіюємо дані, щоб не змінювати оригінал
            df_cleaned = df.copy()

            # Очищення числових даних (Total Charges)
            # Замінюємо порожні рядки на NaN та конвертуємо у float 
            col_charges = self.config.transform.charges_column
            df_cleaned[col_charges] = pd.to_numeric(df_cleaned[col_charges], errors='coerce')
            
            # Заповнюємо пропуски в нарахуваннях нулями (актуально для нових клієнтів) 
            df_cleaned[col_charges] = df_cleaned[col_charges].fillna(0)

            # Обробка пропущених значень у категоріальних даних 
            # Заповнюємо логічні пропуски в причинах відтоку
            fill_values = {
                'Churn Category': 'No Churn',
                'Churn Reason': 'No Churn'
            }
            df_cleaned = df_cleaned.fillna(value=fill_values)

            # Бінаризація цільової змінної (Target) 
            # Створюємо поле is_churn: 1 якщо клієнт пішов, 0 якщо залишився
            target_col = self.config.transform.target_column
            df_cleaned['is_churn'] = df_cleaned[target_col].apply(
                lambda x: 1 if x == 'Churned' else 0
            )

            # Приведення назв колонок до єдиного стилю (snake_case) 
            df_cleaned.columns = [col.lower().replace(' ', '_') for col in df_cleaned.columns]

            # 6. Видалення дублікатів
            initial_count = len(df_cleaned)
            df_cleaned = df_cleaned.drop_duplicates()
            if len(df_cleaned) < initial_count:
                logger.info(f"Видалено {initial_count - len(df_cleaned)} дублікатів.")

            logger.info(f"Трансформація завершена. Підготовлено записів: {len(df_cleaned)}")
            return df_cleaned

        except Exception as e:
            logger.error(f"Помилка на етапі Transform: {e}", exc_info=True)
            raise