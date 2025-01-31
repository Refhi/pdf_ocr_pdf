import os
import time
import shutil
import ocrmypdf
import fitz  # PyMuPDF
import re


def extract_text_from_pdf(pdf_path):
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return ""


def is_text_meaningful(text):
    # Check if the text contains a significant amount of readable characters
    # Here we consider text meaningful if it contains more than 50% alphanumeric characters
    if len(text) == 0:
        return False
    alphanumeric_chars = re.findall(r"\w", text)
    return len(alphanumeric_chars) / len(text) > 0.5


def ocr_pdf_if_needed(input_pdf_path, output_pdf_path):
    extracted_text = extract_text_from_pdf(input_pdf_path)
    if is_text_meaningful(extracted_text):
        print("The PDF already contains readable text. No OCR needed.")
        return False
    else:
        print("The PDF does not contain readable text. Performing OCR...")
        try:
            ocrmypdf.ocr(input_pdf_path, output_pdf_path, force_ocr=True, language='fra')
            return True
        except Exception as e:
            print(f"Error performing OCR on {input_pdf_path}: {e}")
            return None


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


def is_valid_pdf(filename, folder):
    is_valid_extension = (
        filename.endswith(".pdf")
        and not filename.endswith(".ocr.pdf")
        and not filename.endswith(".nocr.pdf")
    )
    if not is_valid_extension:
        return False
    # Check if the file is not empty
    is_valid_size = os.path.getsize(os.path.join(folder, filename)) > 500
    return is_valid_extension and is_valid_size


def get_unique_output_path(folder, filename):
    base_output_pdf_path = os.path.join(folder, filename.replace(".pdf", ".ocr.pdf"))
    output_pdf_path = base_output_pdf_path
    counter = 1
    while os.path.exists(output_pdf_path):
        output_pdf_path = base_output_pdf_path.replace(
            ".ocr.pdf", f"_{counter}.ocr.pdf"
        )
        counter += 1
    return output_pdf_path


def archive_file(file_path, archive_folder, ocr_was_needed):
    if ocr_was_needed:
        shutil.move(
            file_path, os.path.join(archive_folder, os.path.basename(file_path))
        )
        print(f"Archived: {file_path}")
    else:
        print(f"No need to archive: {file_path}")
        rename_file_no_ocr(file_path)


def rename_file_no_ocr(file_path):
    base_new_file_path = file_path.replace('.pdf', '.nocr.pdf')
    new_file_path = base_new_file_path
    counter = 1
    while os.path.exists(new_file_path):
        new_file_path = base_new_file_path.replace('.nocr.pdf', f'_{counter}.nocr.pdf')
        counter += 1
    os.rename(file_path, new_file_path)
    print(f"Renamed file to: {new_file_path}")

def pdf_extension_to_lower_case(filename, folder):
    if filename.endswith(".PDF"):
        os.rename(os.path.join(folder, filename), os.path.join(folder, filename[:-3] + "pdf"))
        print(f"Renamed file to: {filename[:-3] + 'pdf'}")


def process_pdfs(input_folder, archive_folder):
    list_of_files = os.listdir(input_folder)
    date_heure = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{date_heure} - Found {len(list_of_files)} files in {input_folder}")
    for filename in list_of_files:
        pdf_extension_to_lower_case(filename, input_folder)
        if is_valid_pdf(filename, input_folder):
            print(f"Processing: {filename}")
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = get_unique_output_path(input_folder, filename)

            ocr_was_needed = ocr_pdf_if_needed(input_pdf_path, output_pdf_path)
            archive_file(input_pdf_path, archive_folder, ocr_was_needed)


if __name__ == "__main__":
    input_folder = "C:\\scan"
    archive_folder = "C:\\scan\\archive_ocr"

    os.makedirs(archive_folder, exist_ok=True)

    iteration_count = 0

    while True:
        try:
            process_pdfs(input_folder, archive_folder)
            iteration_count += 1
            if iteration_count >= 360:  # donc seulement toutes les heures
                delete_old_archives(archive_folder)
                iteration_count = 0
        except Exception as e:
            print(f"Error processing PDFs: {e}")
        time.sleep(10)
