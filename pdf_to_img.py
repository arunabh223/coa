import fitz 
from PIL import Image
import base64

def convert_pdf_to_images(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate over each page
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_num)
        
        # Get the pixmap (image) of the page
        pix = page.get_pixmap()
        
        # Convert the pixmap to a PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save the image as PNG
        img.save(f"{output_folder}/page_{page_num + 1}.png")

    print("PDF pages have been converted to PNG images.")

pdf_path = 'Vendor%20COA.pdf'
output_folder = '/Users/arunabhbora/Downloads/Code/coa/ext_images'
convert_pdf_to_images(pdf_path, output_folder)
