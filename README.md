# Telecom Churn Project

Проєкт метою якого є зменшення відтоку клієнтів телекомпанії на основі історії користування послугами та звернень до підтримки.

## Запуск ETL процесу

1. **Створіть та активуйте віртуальне середовище:**
```bash
# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```
```shell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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
# Linux/Mac
mkdir -p ~/.kaggle
echo *token_name* > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
```
```shell
# Windows PowerShell
if (!(Test-Path "$HOME\.kaggle")) { New-Item -ItemType Directory -Path "$HOME\.kaggle" }
"*token_name*" | Out-File -FilePath "$HOME\.kaggle\access_token" -Encoding ascii
$path = "$HOME\.kaggle\access_token"
$acl = Get-Acl $path
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME, "FullControl", "Allow")
$acl.AddAccessRule($rule)
Set-Acl $path $acl
```
4. **Запустіть файл main.py, за потреби змінивши вміст файлу конфігурації ``etl_config.yaml``**
```bash
python main.py
```