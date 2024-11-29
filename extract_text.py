import os
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def extract_complete_text(pdf_path):
    """
    Extracts all text from a PDF file using pdfminer.six.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text content.
    """
    try:
        # Define layout parameters for better extraction
        laparams = LAParams()
        
        # Extract text from the entire PDF
        text = extract_text(
            pdf_path,
            laparams=laparams,
            page_numbers=None,  # Extract all pages
            maxpages=0,         # No limit on number of pages
            caching=True,
            codec='utf-8'       # Ensure proper encoding
        )
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def save_text_to_file(pdf_path, text, output_dir):
    """
    Saves extracted text to a .txt file with the same base name as the PDF.

    Args:
        pdf_path (str): Path to the original PDF file.
        text (str): Extracted text content.
        output_dir (str): Directory where the .txt file will be saved.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract the base name without extension
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Define the path for the .txt file
        txt_filename = f"{base_name}.txt"
        txt_path = os.path.join(output_dir, txt_filename)
        
        # Write the extracted text to the .txt file
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Successfully saved extracted text to: {txt_path}")
    except Exception as e:
        print(f"Error saving text to file for {pdf_path}: {e}")

def process_pdfs(input_dir, output_dir):
    """
    Processes all PDF files in the input directory and saves extracted text.

    Args:
        input_dir (str): Directory containing PDF files.
        output_dir (str): Directory where extracted text files will be saved.
    """
    # Verify that the input directory exists
    if not os.path.isdir(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            print(f"\nProcessing '{filename}'...")
            
            # Extract text from the PDF
            text = extract_complete_text(pdf_path)
            
            if text:
                # Save the extracted text to a .txt file
                save_text_to_file(pdf_path, text, output_dir)
                
                # Optionally, print the length of the extracted text
                print(f"Extracted Text Length: {len(text)} characters")
            else:
                print(f"No text extracted from '{filename}'.")

if __name__ == "__main__":
    # Define the input and output directories
    input_pdfs_directory = 'one-pdf'             # Replace with your PDF directory
    output_texts_directory = 'extracted_texts' # Replace with your desired output directory
    
    # Process all PDFs in the input directory
    process_pdfs(input_pdfs_directory, output_texts_directory)
