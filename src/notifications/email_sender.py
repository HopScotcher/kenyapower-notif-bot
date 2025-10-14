import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT
from src.utils.logger import logger

def send_email_notification(recipient_email, outage_details):
    """
    Sends an email notification about a scheduled power outage.

    Args:
        recipient_email (str): The email address of the recipient.
        outage_details (dict): A dictionary containing the parsed outage information.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    if not EMAIL_SENDER_ADDRESS or not EMAIL_SENDER_PASSWORD:
        logger.error("Email sender address or password is not configured in config/settings.py")
        return False

    # --- 1. Format the Email Content ---
    subject = f"Power Outage Alert for {outage_details.get('county', 'your area')}"

    # Create a nice-looking email body
    text_body = f"""
    Hello,

    This is an alert that a power outage has been scheduled that may affect your location.
    Please see the details below:

    County: {outage_details.get('county', 'N/A')}
    Area: {outage_details.get('area', 'N/A')}
    Date: {outage_details.get('date', 'N/A')}
    Time: {outage_details.get('time', 'N/A')}
    Affected Localities: {outage_details.get('localities_affected', 'N/A')}

    This information was sourced from the latest Kenya Power maintenance schedule.
    """

    html_body = f"""
    <html>
    <body>
        <p>Hello,</p>
        <p>This is an alert that a power outage has been scheduled that may affect your location. Please see the details below:</p>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
            <tr><th align="left" style="padding: 8px;">County</th><td style="padding: 8px;">{outage_details.get('county', 'N/A')}</td></tr>
            <tr><th align="left" style="padding: 8px;">Area</th><td style="padding: 8px;">{outage_details.get('area', 'N/A')}</td></tr>
            <tr><th align="left" style="padding: 8px;">Date</th><td style="padding: 8px;">{outage_details.get('date', 'N/A')}</td></tr>
            <tr><th align="left" style="padding: 8px;">Time</th><td style="padding: 8px;">{outage_details.get('time', 'N/A')}</td></tr>
            <tr><th align="left" style="padding: 8px;">Affected Localities</th><td style="padding: 8px;">{outage_details.get('localities_affected', 'N/A')}</td></tr>
        </table>
        <p><em>This information was sourced from the latest Kenya Power maintenance schedule.</em></p>
    </body>
    </html>
    """

    # --- 2. Construct the Email Message ---
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER_ADDRESS
    message["To"] = recipient_email

    # Attach both plain text and HTML versions. Email clients will render the best one.
    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    # --- 3. Connect to the Server and Send ---
    try:
        logger.info(f"Connecting to SMTP server to send email to {recipient_email}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade the connection to a secure one
        server.login(EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD)
        server.sendmail(EMAIL_SENDER_ADDRESS, recipient_email, message.as_string())
        logger.info("Email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP Authentication Error: Failed to login. Check your email and app password in settings.py.")
        return False
    except Exception as e:
        logger.error(f"An error occurred while sending the email: {e}")
        return False
    finally:
        if 'server' in locals() and server:
            server.quit()
