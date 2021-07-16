# Import modules
from PIL import Image
import pytesseract

def ocr(loop):

    # Include tesseract executable in your path
    pytesseract.pytesseract.tesseract_cmd = "OCR/tesseract.exe"

    # Create an image object of PIL library
    # image = input("\nEnter Image name : ")

    image_to_text = []
    for i in range(loop):
        image = Image.open(f'image/plate{i+1}.png')

        # pass image into pytesseract module
        # pytesseract is trained in many languages

        image_to_text.append(pytesseract.image_to_string(image, lang='eng'))

    j=''
    for i in image_to_text:
        j=j+i+'\n'

    return j
