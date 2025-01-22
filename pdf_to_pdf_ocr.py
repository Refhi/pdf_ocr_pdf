import os
import time
import shutil
import ocrmypdf

def ocr_pdf(input_pdf_path, output_pdf_path):
    ocrmypdf.ocr(input_pdf_path, output_pdf_path)

def process_pdfs(input_folder, output_folder, archive_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf') and not filename.endswith('.ocr.pdf'):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, filename.replace('.pdf', '.ocr.pdf'))
            if not os.path.exists(output_pdf_path):
                ocr_pdf(input_pdf_path, output_pdf_path)
                shutil.move(input_pdf_path, os.path.join(archive_folder, filename))

if __name__ == "__main__":
    input_folder = 'tmp'
    output_folder = 'B'
    archive_folder = 'archive'
    
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(archive_folder, exist_ok=True)
    
    while True:
        process_pdfs(input_folder, output_folder, archive_folder)
        time.sleep(10)