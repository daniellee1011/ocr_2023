import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Set the maximum image size to 1 billion pixels
Image.MAX_IMAGE_PIXELS = 1000000000


def extract_first_page_only(pdf_path, dpi_value):
    """
    Extract text from a PDF file using Tesseract OCR and pdf2image.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        org_text (str): Extracted text from the PDF file.
    """
    # Convert the PDF to a list of PIL Image objects
    image = convert_from_path(pdf_path, dpi=dpi_value,
                              first_page=1, last_page=1)[0]
    # image = Image.fromarray(image)

    raw_text = pytesseract.image_to_string(image, config='--oem 3')

    return raw_text


def extract_text_from_pdf(pdf_path, dpi_value):
    """
    Extract text from a PDF file using Tesseract OCR and pdf2image.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        org_text (str): Extracted text from the PDF file.
    """
    # Convert the PDF to a list of PIL Image objects
    images = convert_from_path(pdf_path, dpi=dpi_value)

    text_list = []
    # Loop through each page of the PDF and extract text using Tesseract
    for image in images:
        # print('image')
        raw_text = pytesseract.image_to_string(image, config='--oem 3')
        text_list.append(raw_text)
    # Combine text from all pages into a single string
    org_text = '\n'.join(text_list)
    # print(org_text)
    return org_text
