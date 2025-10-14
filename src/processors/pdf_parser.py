import pdfplumber
import re
from src.utils.logger import logger

def _parse_column_text(text, search_term, page_num):
    """
    A helper function to parse the text from a single column for outage info.
    """
    column_outages = []
    search_term_lower = search_term.lower()
    current_county = "Unknown"
    lines = text.split('\n')

    county_pattern = re.compile(r"PARTS OF (.*?) COUNTY")
    region_pattern = re.compile(r"([\w\s]+) REGION")
    area_pattern = re.compile(r"AREA:\s*(.*)")
    date_pattern = re.compile(r"DATE:\s*(.*)")
    time_pattern = re.compile(r"TIME:\s*(.*)")

    for i, line in enumerate(lines):
        county_match = county_pattern.search(line)
        if county_match:
            current_county = county_match.group(1).strip()
            continue

        region_match = region_pattern.search(line)
        if region_match and "REGION" in line and not county_match:
            current_county = region_match.group(1).strip()
            continue

        area_match = area_pattern.search(line)
        if area_match:
            area = area_match.group(1).strip()
            # Reset details for each new area found
            date = "Not Found"
            time = "Not Found"
            localities = []

            # Date and Time can be on the same line as Area, or on the next line
            full_area_line = line
            if i + 1 < len(lines):
                full_area_line += " " + lines[i+1] # Combine with next line for robustness

            date_match = date_pattern.search(full_area_line)
            if date_match:
                date = date_match.group(1).strip()

            time_match = time_pattern.search(full_area_line)
            if time_match:
                time = time_match.group(1).strip()

            # Localities start after the AREA/DATE/TIME lines
            j = 1
            # Skip the line containing TIME if it's separate
            if i + j < len(lines) and "TIME:" in lines[i+j]:
                j += 1
                
            while (i + j) < len(lines) and lines[i+j].strip() and "AREA:" not in lines[i+j] and "For further" not in lines[i+j] and "COUNTY" not in lines[i+j] and "REGION" not in lines[i+j]:
                localities.append(lines[i+j].strip())
                j += 1

            localities_str = ' '.join(localities)

            if (search_term_lower in current_county.lower() or
                search_term_lower in area.lower() or
                search_term_lower in localities_str.lower()):

                outage_details = {
                    "county": current_county,
                    "area": area,
                    "date": date,
                    "time": time,
                    "localities_affected": localities_str
                }
                column_outages.append(outage_details)
                logger.info(f"Match found for '{search_term}' in {current_county} on page {page_num}!")
    
    return column_outages


def parse_pdf(pdf_path, search_term):
    """
    Parses a two-column PDF by cropping each page into two halves and
    processing them independently to prevent data mixing.
    """
    logger.info(f"Parsing PDF: {pdf_path} for location: '{search_term}'")
    found_outages = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Define the bounding box for the left and right columns
                width = page.width
                height = page.height
                midpoint = width / 2
                
                # Bounding box format: (x0, top, x1, bottom)
                left_bbox = (0, 0, midpoint, height)
                right_bbox = (midpoint, 0, width, height)

                # Crop the page and extract text from each column
                left_column = page.crop(left_bbox)
                right_column = page.crop(right_bbox)

                left_text = left_column.extract_text()
                right_text = right_column.extract_text()

                # Parse each column's text independently
                if left_text:
                    found_in_left = _parse_column_text(left_text, search_term, page_num)
                    found_outages.extend(found_in_left)
                
                if right_text:
                    found_in_right = _parse_column_text(right_text, search_term, page_num)
                    found_outages.extend(found_in_right)

    except Exception as e:
        logger.error(f"Failed to parse PDF {pdf_path}. Error: {e}")

    if not found_outages:
        logger.info(f"No scheduled outages found for '{search_term}' in {pdf_path}.")

    return found_outages

 





# import fitz
# import re
# from src.utils.logger import logger


# def parse_pdf(pdf_path, location):
#     """
#     Parse PDF for power maintenance notices and find matching location paragraph.

#     Args:
#         pdf_path (str): Path to the PDF file
#         location (str): Location name to search for

#     Returns:
#         bool: True if location found, False otherwise
#     """
#     try:
#         # Open the PDF document
#         doc = fitz.open(pdf_path)

#         # Extract text from all pages
#         full_text = ""
#         for page_num in range(len(doc)):
#             page = doc.load_page(page_num)
#             full_text += page.get_text()

#         doc.close()

#         # Split text into paragraphs based on the pattern observed
#         # Each area section starts with "AREA:" and ends before the next "AREA:" or end of text
#         area_pattern = r"AREA:\s*([^\n]+(?:\n(?!AREA:)[^\n]*)*)"
#         area_matches = re.findall(area_pattern, full_text, re.MULTILINE | re.DOTALL)

#         # Also split by double line breaks to catch other paragraph structures
#         paragraphs = full_text.split("\n\n")

#         # Combine both methods to ensure we catch all relevant sections
#         all_sections = area_matches + paragraphs

#         # Search for the location in each section (partial matches allowed)
#         location_found = False
#         for section in all_sections:
#             if location.lower() in section.lower():
#                 # Clean up the section text
#                 cleaned_section = section.strip()
#                 if cleaned_section:  # Only log non-empty sections
#                     logger.info(
#                         f"Partial match for '{location}' found in maintenance notice:"
#                     )
#                     logger.info(f"\n{cleaned_section}")
#                     location_found = True
#                     break

#         if not location_found:
#             logger.info(f"Location '{location}' not found in maintenance notices.")

#         return location_found

#     except Exception as e:
#         logger.error(f"Error parsing PDF: {str(e)}")
#         return False
