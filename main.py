import os
from src.scrapers.pdf_downloader import download_pdfs
from src.processors.pdf_parser import parse_pdf
# from src.notifications.email_sender import send_email
# from src.database.db_manager import setup_database, add_user, get_users
from src.utils.logger import logger


def main():
    logger.info("Kenya Power Notifier started.")

    # Initialize database
    # setup_database()

    # Download PDFs from Kenya Power website
    pdf_files = download_pdfs()
    location = "Redcross"

    # Parse PDFs and check for relevant locations
    for pdf_file in pdf_files:
        matched_locations = parse_pdf(pdf_file, location)

        if matched_locations:
            print(f"Scheduled outage in {location}")
            # users = get_users()
            # for user in users:
            #     if user.location in matched_locations:
            #         send_email(user.email, "Power Outage Alert", f"Scheduled outage in {user.location}")

    logger.info("Kenya Power Notifier finished.")


if __name__ == "__main__":
    main()
