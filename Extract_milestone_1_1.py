import fitz  # PyMuPDF
import re

def is_table_present(text):
    """
    Checks if a table is present in the text by looking for patterns.
    This function can be modified based on how the tables in the PDF are structured.
    """
    # Regex pattern for table-like text (e.g., numbers or words separated by multiple spaces or tab)
    table_pattern = re.compile(r'(\S+\s{2,}\S+)')
    # Check if the pattern matches any part of the page text
    if table_pattern.search(text):
        return True
    return False

def extract_pages_with_tables(pdf_path, output_path):
    """
    Extracts pages from the PDF that contain tables and saves them to a new PDF.
    """
    # Open the PDF
    doc = fitz.open(pdf_path)
    new_pdf = fitz.open()

    # Track whether any pages were added
    pages_with_tables = 0

    # Iterate through the pages of the document
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load page
        text = page.get_text("text")    # Extract the text of the page
        
        if is_table_present(text):      # Check if the page contains a table
            print(f"Table detected on page {page_num + 1}")  # Inform user that table was found
            new_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)
            pages_with_tables += 1

    # Save the new PDF only if pages were added
    if pages_with_tables > 0:
        new_pdf.save(output_path)
        print(f"Saved {pages_with_tables} pages containing tables to {output_path}")
    else:
        print("No pages with tables were found.")
    
    new_pdf.close()
    doc.close()

# Example usage:
pdf_path = 'yellow.pdf'
output_path = 'output_with_tables.pdf'
extract_pages_with_tables(pdf_path, output_path)
