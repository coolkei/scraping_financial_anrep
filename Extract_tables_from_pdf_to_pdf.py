import pdfplumber
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Function to extract tables from a PDF
def extract_tables_from_pdf(input_pdf_path):
    tables = []
    
    # Open the input PDF
    with pdfplumber.open(input_pdf_path) as pdf:
        # Loop through each page
        for page in pdf.pages:
            # Extract tables from each page
            tables_on_page = page.extract_tables()
            if tables_on_page:
                for table in tables_on_page:
                    # Check if the table has enough rows (i.e., at least a header and one row of data)
                    if len(table) > 1 and all(table[0]):  # Ensure the first row (header) is not empty
                        try:
                            df = pd.DataFrame(table[1:], columns=table[0])  # Convert to DataFrame for clean formatting
                            tables.append(df)
                        except Exception as e:
                            print(f"Error creating DataFrame: {e}")
                            continue  # Skip the problematic table
                    else:
                        print("Skipping table due to missing or empty header.")
                    
    return tables

# Function to write tables to a new PDF using the Table class
def write_tables_to_pdf(tables, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    elements = []

    for df in tables:
        # Convert the DataFrame to a list of lists (data format required for reportlab Table)
        table_data = [df.columns.tolist()] + df.values.tolist()

        # Create a Table
        table = Table(table_data)

        # Add table style for formatting (optional)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Add the table to the elements to be written to the PDF
        elements.append(table)
        elements.append(Spacer(1, 12))  # Add space after each table

    # Build the PDF
    doc.build(elements)

# Main execution
input_pdf_path = "D:/Second/scripts/yellow.pdf"  # Replace this with the correct file path
output_pdf_path = "D:/Second/scripts/output_tables_only_v2.pdf"  # Ensure the output path is correct too

# Extract tables
tables = extract_tables_from_pdf(input_pdf_path)

# Write the extracted tables to a new PDF
write_tables_to_pdf(tables, output_pdf_path)

print(f"Tables extracted and saved to {output_pdf_path}")
