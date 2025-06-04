import requests
from bs4 import BeautifulSoup
import os
from src.utils.logger import logger

PDF_DIRECTORY = "data/pdfs"
KENYA_POWER_URL = "https://www.kplc.co.ke/customer-support#powerschedule"


def download_pdfs():
    try:
        response = requests.get(KENYA_POWER_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        pdf_div = soup.find('div', id='powerschedule')
        
         # Find all 'a' tags within that div and extract the href attribute if it ends with .pdf
        pdf_links = [link.get('href') for link in pdf_div.find_all('a') if link.get('href', '').endswith('.pdf')]
        
        if not pdf_links:
            logger.warning("No PDFs found on the website.")
            return []

        latest_pdf_url = pdf_links[0]  # Always get the latest PDF
        pdf_name = latest_pdf_url.split('/')[-1]
        pdf_path = os.path.join(PDF_DIRECTORY, pdf_name)

        if not os.path.exists(PDF_DIRECTORY):
            os.makedirs(PDF_DIRECTORY)

        if os.path.exists(pdf_path):
            logger.info(f"Latest PDF already exists locally: {pdf_name}")
            return [pdf_path]

        # Download the latest PDF
        pdf_response = requests.get(latest_pdf_url)
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)

        logger.info(f"Downloaded latest PDF: {pdf_name}")
        return [pdf_path]

    except requests.RequestException as e:
        logger.error(f"Error fetching PDFs: {e}")
        return []


# import requests
# from bs4 import BeautifulSoup
# import os
# from src.utils.logger import logger

# PDF_DIRECTORY = "data/pdfs"
# KENYA_POWER_URL = 


# def download_pdfs():
#     try:
#         response = requests.get(KENYA_POWER_URL)
#         response.raise_for_status()

#         soup = BeautifulSoup(response.text, 'lxml')
#         pdf_div = soup.find('div', id='powerschedule')

        
#         # Find all 'a' tags within that div and extract the href attribute if it ends with .pdf
#         pdf_links = [link.get('href') for link in pdf_div.find_all('a') if link.get('href', '').endswith('.pdf')]
        

#         if not pdf_links:
#             logger.warning("No PDFs found on the website.")
#             return []

#         latest_pdf_url = pdf_links[0]  # Always get the latest PDF
#         pdf_name = latest_pdf_url.split('/')[-1]
#         pdf_path = os.path.join(PDF_DIRECTORY, pdf_name)

#         if not os.path.exists(PDF_DIRECTORY):
#             os.makedirs(PDF_DIRECTORY)

#         # Download the latest PDF
#         pdf_response = requests.get(latest_pdf_url)
#         with open(pdf_path, 'wb') as pdf_file:
#             pdf_file.write(pdf_response.content)

#         logger.info(f"Downloaded latest PDF: {pdf_name}")
#         return [pdf_path]

#     except requests.RequestException as e:
#         logger.error(f"Error fetching PDFs: {e}")
#         return []
    