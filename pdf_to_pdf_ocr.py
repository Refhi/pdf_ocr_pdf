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

def is_valid_pdf(filename):
    return (filename.endswith('.pdf') and not filename.endswith('.ocr.pdf') and 
            ('img' in filename or 'Scan' in filename))

def get_unique_output_path(folder, filename):
    base_output_pdf_path = os.path.join(folder, filename.replace('.pdf', '.ocr.pdf'))
    output_pdf_path = base_output_pdf_path
    counter = 1
    while os.path.exists(output_pdf_path):
        output_pdf_path = base_output_pdf_path.replace('.ocr.pdf', f'_{counter}.ocr.pdf')
        counter += 1
    return output_pdf_path

def archive_file(file_path, archive_folder):
    shutil.move(file_path, os.path.join(archive_folder, os.path.basename(file_path)))

def process_pdfs(input_folder, archive_folder):
    for filename in os.listdir(input_folder):
        if is_valid_pdf(filename):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = get_unique_output_path(input_folder, filename)
            
            ocr_pdf(input_pdf_path, output_pdf_path)
            archive_file(input_pdf_path, archive_folder)




if __name__ == "__main__":
    input_folder = 'S:\\'
    archive_folder = 'S:\\archive_ocr'

    
    os.makedirs(archive_folder, exist_ok=True)
    
    iteration_count = 0
    
    while True:
        process_pdfs(input_folder, archive_folder)
        iteration_count += 1
        if iteration_count >= 360: # donc seulement toutes les heures
            delete_old_archives(archive_folder)
            iteration_count = 0
        time.sleep(10)