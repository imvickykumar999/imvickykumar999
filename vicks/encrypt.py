from PIL import Image
import os, PyPDF2, img2pdf

# img_path = "download.jpg"
# pdf_path = "Django_Models.pdf"
# encrypt = 'encrypted_output.pdf'

def imgtopdf(img_path = "imvickykumar999.jpg"):
    image = Image.open(img_path)
    pdf_bytes = img2pdf.convert(image.filename)

    pdfile = f"{img_path.split('.')[0]}.pdf"
    file = open(pdfile, "wb")
    file.write(pdf_bytes)

    image.close()
    file.close()
    return pdfile

def encryptpdf(pdf_path = "imvickykumar999.pdf", passw = 'pass'):
    pdfFile = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pdfWriter = PyPDF2.PdfFileWriter()

    for pageNum in range(pdfReader.numPages):
        pdfWriter.addPage(pdfReader.getPage(pageNum))

    # passw = input('Enter password to set : ')
    pdfWriter.encrypt(passw)
    fil = f'{pdf_path.split(".")[0]}_encrypted.pdf'

    resultPdf = open(fil, 'wb')
    pdfWriter.write(resultPdf)
    resultPdf.close()
    return fil

# imgtopdf(img_path)
# encryptpdf(pdf_path)
# os.startfile(encrypt)
