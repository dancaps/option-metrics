import PyPDF2

# Path to the PDF file
pdf_path = '../project_requirements/OptionsDataTask.pdf'
output_path = '../project_requirements/OptionsDataTask.txt'

# Open the PDF file
with open(pdf_path, 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    with open(output_path, 'w') as output_file:
        for page in reader.pages:
            text = page.extract_text()
            if text:
                output_file.write(text + '\n')

print(f"PDF content has been saved to {output_path}")