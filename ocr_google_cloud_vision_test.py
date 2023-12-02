import io
import os
import sys
from pdf2image import convert_from_path
from google.cloud import vision
from PIL import Image
import sys


def convert_pdf_to_image(pdf_file):
    # Convert a PDF file to an image
    return convert_from_path(pdf_file, dpi=200)


def detect_text(image, output_txt_path):
    # Detects text in an image file and saves the details including confidences.
    client = vision.ImageAnnotatorClient()

    with io.BytesIO() as output:
        image.save(output, format="JPEG")
        content = output.getvalue()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    # Initialize a variable to store the extracted text with confidence levels
    extracted_text = ""

    if response.error.message:
        raise Exception(
            f'{response.error.message}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors')

    # Iterate over text detections and append them with confidence levels to the extracted_text
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            extracted_text += f'Block confidence: {block.confidence}\n'
            for paragraph in block.paragraphs:
                extracted_text += f'\tParagraph confidence: {paragraph.confidence}\n'
                for word in paragraph.words:
                    word_text = ''.join(
                        [symbol.text for symbol in word.symbols])
                    word_confidence = word.confidence
                    extracted_text += f'\t\tWord text: {word_text} (confidence: {word_confidence})\n'
                extracted_text += '\n'
            extracted_text += '\n'

    # Write the structured text with confidence levels to a file
    with open(output_txt_path, 'w', encoding='utf-8') as file:
        file.write(extracted_text)


def main(directory):
    pdf_files = [f for f in os.listdir(
        directory) if f.lower().endswith('.pdf') and '1992' in f]
    # Process only the first twenty PDF files
    for pdf_file in sorted(pdf_files)[:20]:
        pdf_path = os.path.join(directory, pdf_file)
        images = convert_pdf_to_image(pdf_path)
        for i, image in enumerate(images):
            # Define the path for the output text file
            text_filename = os.path.splitext(pdf_file)[0] + f'_page_{i+1}.txt'
            text_file_path = os.path.join(directory, text_filename)

            # Call the detect_text function and pass the path to save the text
            detect_text(image, text_file_path)

            print(
                f'Saved detailed text of {pdf_file} page {i+1} to {text_filename}')


def _main(pdf_file):
    images = convert_pdf_to_image(pdf_file)
    for image in images:
        detect_text(image)


if __name__ == "__main__":
    # pdf_file = sys.argv[1]
    # main(pdf_file)
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(directory)
