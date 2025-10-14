import os

# Directories
PDF_DIRECTORY = "data/pdfs"
LOG_FILE_PATH = "logs/app.log"
DB_PATH = "data/database.sqlite"

# Kenya Power Website
KENYA_POWER_URL = "https://kenyapower.co.ke/outages"

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


# Your email credentials and SMTP server details.
# IMPORTANT: For Gmail, you MUST use an "App Password", not your regular password.
# See instructions here: https://support.google.com/accounts/answer/185833

# Sender's email details
EMAIL_SENDER_ADDRESS = "info.advendigital@gmail.com"  # Your full email address
EMAIL_SENDER_PASSWORD = "iawzwltteicnsomk "  # Your 16-digit App Password

# SMTP Server configuration (using Gmail as an example)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # For TLS

