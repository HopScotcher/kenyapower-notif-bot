import fitz
import re
from src.utils.logger import logger


def parse_pdf(pdf_path, location):
    """
    Parse PDF for power maintenance notices and find matching location paragraph.

    Args:
        pdf_path (str): Path to the PDF file
        location (str): Location name to search for

    Returns:
        bool: True if location found, False otherwise
    """
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)

        # Extract text from all pages
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text()

        doc.close()

        # Split text into paragraphs based on the pattern observed
        # Each area section starts with "AREA:" and ends before the next "AREA:" or end of text
        area_pattern = r"AREA:\s*([^\n]+(?:\n(?!AREA:)[^\n]*)*)"
        area_matches = re.findall(area_pattern, full_text, re.MULTILINE | re.DOTALL)

        # Also split by double line breaks to catch other paragraph structures
        paragraphs = full_text.split("\n\n")

        # Combine both methods to ensure we catch all relevant sections
        all_sections = area_matches + paragraphs

        # Search for the location in each section (partial matches allowed)
        location_found = False
        for section in all_sections:
            if location.lower() in section.lower():
                # Clean up the section text
                cleaned_section = section.strip()
                if cleaned_section:  # Only log non-empty sections
                    logger.info(
                        f"Partial match for '{location}' found in maintenance notice:"
                    )
                    logger.info(f"\n{cleaned_section}")
                    location_found = True
                    break

        if not location_found:
            logger.info(f"Location '{location}' not found in maintenance notices.")

        return location_found

    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        return False


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

#             # Split text into paragraphs based on double line breaks
#             paragraphs = re.split(r"\n{2,}", text)

#             # for para in paragraphs:
#             #     if re.search(rf"\b{location}\b", para, re.IGNORECASE):
#             #         relevant_paragraphs.append(para.strip())

#             for paragraph in paragraphs:
#                 if location.lower() in paragraph.lower():
#                     print(paragraph)
#                     break

#         document.close()

#         if relevant_paragraphs:
#             logger.info(
#                 f"Found {len(relevant_paragraphs)} matching paragraphs for {location}"
#             )
#             for para in relevant_paragraphs:
#                 logger.info(f"Paragraph: {para}")

#         else:
#             logger.info(f"No matches found for {location}")

#         # return relevant_paragraphs

#     except Exception as e:
#         logger.error(f"Error parsing PDF: {e}")
#         return []


# NEW CODE
# import fitz  # PyMuPDF
# import re
# from src.utils.logger import logger

# def parse_pdf(pdf_path, location):
#     try:
#         with fitz.open(pdf_path) as document:
#             extracted_blocks = []
#             seen_blocks = set()

#             for page in document:
#                 text = page.get_text()
#                 paragraphs = re.split(r'\n{2,}', text)

#                 # Identify all indices where location appears
#                 match_indices = [i for i, para in enumerate(paragraphs) if re.search(rf"\b{re.escape(location)}\b", para, re.IGNORECASE)]

#                 for idx in match_indices:
#                     # Traverse upwards
#                     start_idx = idx
#                     while start_idx > 0 and paragraphs[start_idx - 1].lstrip().startswith("AREA:"):
#                         start_idx -= 1

#                     # Traverse downwards
#                     end_idx = idx
#                     while end_idx < len(paragraphs) - 1 and paragraphs[end_idx + 1].lstrip().startswith("AREA:"):
#                         end_idx += 1

#                     # Combine the block
#                     block_paras = paragraphs[start_idx:end_idx + 1]
#                     block = "\n\n".join(p.strip() for p in block_paras)

#                     if block not in seen_blocks:
#                         seen_blocks.add(block)
#                         extracted_blocks.append(block)

#         if extracted_blocks:
#             logger.info(f"Found {len(extracted_blocks)} matching blocks for {location}")
#             for block in extracted_blocks:
#                 logger.info(f"Block:\n{block}")
#         else:
#             logger.info(f"No matches found for {location}")

#         return extracted_blocks

#     except Exception as e:
#         logger.error(f"Error parsing PDF: {e}")
#         return []
