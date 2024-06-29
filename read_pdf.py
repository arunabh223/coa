import pymupdf

# Open the PDF document
doc = pymupdf.open("/Users/arunabhbora/Downloads/Code/coa/VendorCOA.pdf")

# Open a file to save the extracted text
with open("output.txt", "w", encoding="utf-8") as output_file:
    # Iterate over each page and extract text
    for page in doc:
        text = page.get_text()
        output_file.write(text)
        output_file.write("\n\n")  # Add a newline between pages