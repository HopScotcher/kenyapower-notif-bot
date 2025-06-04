import os

# Directories
PDF_DIRECTORY = "data/pdfs"
LOG_FILE_PATH = "logs/app.log"
DB_PATH = "data/database.sqlite"

# Kenya Power Website
KENYA_POWER_URL = "https://kenyapower.co.ke/outages"

# Notification Settings
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "user@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "securepassword")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@example.com")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
