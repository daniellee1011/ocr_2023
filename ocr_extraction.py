import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError
import numpy as np
import cv2
import os
from subprocess import check_output, CalledProcessError, STDOUT
from spellchecker import SpellChecker


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Set the maximum image size to 1 billion pixels
Image.MAX_IMAGE_PIXELS = 1000000000
custom_oem_psm_config = r'--oem 3 --psm 6'


def extract_first_page_only(pdf_path, dpi_value):
    """
    Extract text from a PDF file using Tesseract OCR and pdf2image.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        org_text (str): Extracted text from the PDF file.
    """
    # Convert the PDF to a list of PIL Image objects
    try:
        image = convert_from_path(pdf_path, dpi=dpi_value,
                                  first_page=1, last_page=1)[0]
    except PDFPageCountError as e:
        print(f"Error processing the PDF: {e}")
        return None

    raw_text = pytesseract.image_to_string(image)

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
    # images = convert_from_path(pdf_path, dpi=dpi_value)
    try:
        images = convert_from_path(pdf_path, dpi=dpi_value)
    except PDFPageCountError as e:
        print(f"Error processing the PDF: {e}")
        return None

    image_folder = './segment_image'
    if not os.path.exists('./segment_image'):
        os.makedirs('./segment_image')

    # Loop through each page of the PDF and extract text using Tesseract
    text_list = []
    cnt = 1
    for image in images:
        # Convert PIL image to OpenCV format
        opencv_image = np.array(image)

        gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(
            gray_image, 128, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((25, 35), np.uint8)
        dilated = cv2.dilate(binary, kernel, iterations=2)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sorted_countours = sorted(
            contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
        for contour in sorted_countours:
            x, y, w, h = cv2.boundingRect(contour)
            segment = gray_image[y:y+h, x:x+w]
            text = pytesseract.image_to_string(
                segment, config=custom_oem_psm_config)
            text_list.append(text)

            cv2.rectangle(gray_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        resized_image = cv2.resize(gray_image, (int(
            gray_image.shape[1] * 0.5), int(gray_image.shape[0] * 0.5)))
        base_name = os.path.basename(pdf_path).replace('.pdf', '')
        image_name = base_name + '_' + str(cnt) + '.png'
        full_path = os.path.join(image_folder, image_name)
        cv2.imwrite(full_path, resized_image)
        # cv2.destroyAllWindows()
        cnt += 1

    # Combine text from all pages into a single string
    org_text = '\n'.join(text_list)

    return org_text


def correct_spelling(text):
    spell = SpellChecker()
    # Find all words in the text
    words = text.split()
    # Find those words that may be misspelled
    misspelled = spell.unknown(words)

    for word in misspelled:
        # Get the one `most likely` answer
        correct_word = spell.correction(word)
        # If correct_word is None, which is unexpected, skip replacement
        if correct_word is not None:
            # Replace the misspelled word in the original text with the correct word
            text = text.replace(word, correct_word)

    return text
