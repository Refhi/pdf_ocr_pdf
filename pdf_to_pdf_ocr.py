import os
import time
import shutil
import ocrmypdf

def ocr_pdf(input_pdf_path, output_pdf_path):
    ocrmypdf.ocr(input_pdf_path, output_pdf_path)

def delete_old_archives(archive_folder, days=30):
    now = time.time()
    cutoff = now - (days * 86400)

    for filename in os.listdir(archive_folder):
        file_path = os.path.join(archive_folder, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff:
                os.remove(file_path)
                print(f"Deleted old archive: {file_path}")

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
    
    iteration_count = 0
    
    while True:
        process_pdfs(input_folder, output_folder, archive_folder)
        iteration_count += 1
        if iteration_count >= 360: # donc seulement toutes les heures
            delete_old_archives(archive_folder)
            iteration_count = 0
        time.sleep(10)