import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_tables_with_pdfplumber(input_pdf_path, output_pdf_path):
    with pdfplumber.open(input_pdf_path) as pdf:
        # Create a new PDF to store the tables
        output_canvas = canvas.Canvas(output_pdf_path, pagesize=letter)

        for page_num, page in enumerate(pdf.pages):
            # Extract tables from each page
            tables = page.extract_tables()

            if tables:
                output_canvas.drawString(100, 750, f"Page {page_num + 1} Tables")

                for i, table in enumerate(tables):
                    output_canvas.drawString(100, 730 - (i * 20), str(table))

                output_canvas.showPage()

    output_canvas.save()
    print(f"Extracted tables have been saved to {output_pdf_path}")

# Example usage
input_pdf = "D:/Second/scripts/PDFs/Yellow Corporation 2022 Annual Report.pdf"
output_pdf = "extracted_tables_with_pdfplumber.pdf"
extract_tables_with_pdfplumber(input_pdf, output_pdf)