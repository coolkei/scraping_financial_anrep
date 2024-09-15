import fitz  # PyMuPDF
import camelot
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\gs\gs10.03.1\bin"

def extract_tables_from_pdf(input_pdf, output_pdf):
    # Open the input PDF
    pdf_document = fitz.open(input_pdf)

    # Prepare a new PDF for output
    new_pdf = fitz.open()

    # Loop through all pages of the input PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        # Extract tables using Camelot in lattice mode to maintain table structure
        tables = camelot.read_pdf(input_pdf, pages=str(page_num + 1), flavor='stream')

        # Skip plain text and extract only tables
        if len(tables) > 0:
            for table in tables:
                # Convert table into a list of lists (to retain structure)
                table_data = table.df.values.tolist()

                # Create a new blank page for each table
                new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)

                # Insert the extracted table row by row (you can adjust coordinates as needed)
                y_offset = 72
                for row in table_data:
                    row_text = " | ".join(row)  # Convert row to a string with columns separated
                    new_page.insert_text((72, y_offset), row_text, fontsize=10, fontname="Courier")
                    y_offset += 15  # Adjust row spacing

    # Save the new PDF with only tables
    new_pdf.save(output_pdf)
    new_pdf.close()
    pdf_document.close()

# Input and output PDF paths
input_pdf = "yellow.pdf"  # Replace with your actual file
output_pdf = "tables_only.pdf"  # Output path for tables only

# Extract tables and save to the new PDF
extract_tables_from_pdf(input_pdf, output_pdf)

print(f"Tables extracted and saved to {output_pdf}")