import os
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdf2image import convert_from_path
from PIL import Image
import pytesseract # Tesseract OCR




def extract_complete_text(pdf_path):
    """
    Extracts all text from a PDF file using pdfminer.six.
    Additionally performs OCR on images within the PDF.
    """
    try:
        # Extract text using pdfminer.six
        laparams = LAParams()
        text = extract_text(
            pdf_path,
            laparams=laparams,
            page_numbers=None,
            maxpages=0,
            caching=True,
            codec='utf-8'
        )
        
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        print(f"Converted PDF to {len(images)} image(s) for OCR.")
        
        # Perform OCR on each image and append to text
        for i, image in enumerate(images, start=1):
            ocr_text = pytesseract.image_to_string(image)
            text += f"\n\n--- OCR Text from Page {i} ---\n{ocr_text}"
        
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def save_text_to_file(pdf_path, text, output_dir):
    """
    Saves extracted text to a .txt file with the same base name as the PDF.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        txt_filename = f"{base_name}.txt"
        txt_path = os.path.join(output_dir, txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        print(f"Text saved to {txt_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")
        
def process_pdf(input_dir, output_dir):
    """
    Processes PDF files in a directory by extracting text and saving it to .txt files.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a valid directory.")
        return

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            print(f"\nProcessing {filename}'...") # Print statement for debugging
            text = extract_complete_text(pdf_path)
            if text:
                save_text_to_file(pdf_path, text, output_dir)
                print(f"Extracted Text Length: {len(text)} characters")
            else:
                print(f"No text extracted from {pdf_path}")
                    
if __name__ == "__main__":  
    input_dir = "one-pdf" # Directory containing PDF files
    output_dir = "extracted_texts"  # Directory to save extracted text files
    process_pdf(input_dir, output_dir)