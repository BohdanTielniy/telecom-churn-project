import logging
import sys
from pathlib import Path

def setup_logger(log_file_path: Path):
    """
    Налаштовує систему логування для всього проєкту.
    """
    # Створюємо папку для логів, якщо її немає
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Формат повідомлень: Час - Назва модуля - Рівень - Повідомлення
    log_format = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обробник для запису у файл
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(log_format)

    # Обробник для виводу в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    # Налаштування кореневого логера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Очищаємо попередні обробники, щоб уникнути дублювання при перезапусках
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)