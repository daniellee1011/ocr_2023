import io
from pdf2image import convert_from_path
from google.cloud import vision
from PIL import Image
import sys


def convert_pdf_to_image(pdf_file):
    """ Convert a PDF file to an image """
    return convert_from_path(pdf_file, dpi=200)


def detect_text(image):
    """ Detects text in an image file """
    client = vision.ImageAnnotatorClient()

    with io.BytesIO() as output:
        image.save(output, format="JPEG")
        content = output.getvalue()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))
            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(paragraph.confidence))
                for word in paragraph.words:
                    word_text = ''.join(
                        [symbol.text for symbol in word.symbols])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

    if response.error.message:
        raise Exception(
            f'{response.error.message}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors')


def main(pdf_file):
    images = convert_pdf_to_image(pdf_file)
    for image in images:
        detect_text(image)


if __name__ == "__main__":
    pdf_file = sys.argv[1]
    main(pdf_file)
