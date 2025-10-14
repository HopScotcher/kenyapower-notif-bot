import os
from src.scrapers.pdf_downloader import download_pdfs
from src.processors.pdf_parser import parse_pdf
from src.notifications.email_sender import (
    send_email_notification,
)  # <-- Import the new function
from src.utils.logger import logger


def main():
    logger.info("Kenya Power Notifier started.")

    # --- Configuration ---
    # In a real app, this would come from a user database
    user_location_to_check = "Nyeri"
    user_email_to_notify = (
        "brianndolo846@gmail.com"  # <-- The email address to send the alert to
    )

    pdf_files = download_pdfs()

    if not pdf_files:
        logger.info("No new PDFs to process. Exiting.")
        return

    latest_pdf = pdf_files[0]
    matched_locations = parse_pdf(latest_pdf, user_location_to_check)

    if matched_locations:
        logger.info(
            f"Found {len(matched_locations)} scheduled outage(s) for '{user_location_to_check}'."
        )

        for outage in matched_locations:
            print("\n--- POWER OUTAGE ALERT ---")
            print(f"  County:     {outage['county']}")
            print(f"  Area:       {outage['area']}")
            print(f"  Date:       {outage['date']}")
            print(f"  Time:       {outage['time']}")
            print(f"  Localities: {outage['localities_affected']}")
            print("--------------------------\n")

            # --- Send the email for each found outage ---
            logger.info(f"Sending notification to {user_email_to_notify}...")
            send_email_notification(user_email_to_notify, outage)

    else:
        logger.info(
            f"No matches for '{user_location_to_check}' found in {os.path.basename(latest_pdf)}."
        )

    logger.info("Kenya Power Notifier finished.")


if __name__ == "__main__":
    main()
