# import fitz  # PyMuPDF
# import re
# from src.utils.logger import logger


# def parse_pdf(pdf_path, location):
#     try:
#         document = fitz.open(pdf_path)
#         relevant_paragraphs = []

#         for page_num in range(len(document)):
#             page = document.load_page(page_num)
#             text = page.get_text()

#             # Search for the location and get associated paragraph
#             pattern = rf"(.*?\b{location}\b.*?\n(?:.*?\n)*)"
#             matches = re.findall(pattern, text, re.IGNORECASE)

#             if matches:
#                 relevant_paragraphs.extend(matches)

#         document.close()

#         if relevant_paragraphs:
#             logger.info(f"Found {len(relevant_paragraphs)} matching paragraphs for {location}")
#         else:
#             logger.info(f"No matches found for {location}")

#         return relevant_paragraphs

#     except Exception as e:
#         logger.error(f"Error parsing PDF: {e}")
#         return []
    
    
    
import fitz  # PyMuPDF
import re
from src.utils.logger import logger


def parse_pdf(pdf_path, location):
    try:
        document = fitz.open(pdf_path)
        relevant_paragraphs = []

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text = page.get_text()

            # Split text into paragraphs based on double line breaks
            paragraphs = re.split(r'\n{2,}', text)

            for para in paragraphs:
                if re.search(rf"\b{location}\b", para, re.IGNORECASE):
                    relevant_paragraphs.append(para.strip())

        document.close()

        if relevant_paragraphs:
            logger.info(f"Found {len(relevant_paragraphs)} matching paragraphs for {location}")
        else:
            logger.info(f"No matches found for {location}")

        return logger.info(relevant_paragraphs)

    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        return []

