# Telecom Churn Project

Проєкт метою якого є зменшення відтоку клієнтів телекомпанії на основі історії користування послугами та звернень до підтримки.

## Як запустити

1. **Створіть та активуйте віртуальне середовище:**
```bash
python -m venv .venv

# Для Windows:
.venv\Scripts\activate

# Для Linux/Mac:
source .venv/bin/activate
```
2. **Встановіть залежності**
```bash
pip install -r requirements.txt
```
3. **Створіть файл kaggle.json**

- Увійдіть в свій акаунт на [Kaggle](https://www.kaggle.com/)
- Натисніть на фото свого профілю у верхньому правому куті та виберіть **Settings**.
- Оберіть розділ **API Tokens**.
- Натисніть кнопку **Generate New Token**.
- Назвіть його ``kagle``
- Збережіть його в ``~/.kaggle/access_token``
```bash
mkdir -p ~/.kaggle
echo *token_name* > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
```
