import pdfplumber
import csv

def extract_tables_to_csv(input_pdf_path, output_csv_path):
    with pdfplumber.open(input_pdf_path) as pdf:
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            for page_num, page in enumerate(pdf.pages):
                # Extract tables from each page
                tables = page.extract_tables()

                if tables:
                    for table in tables:
                        writer.writerows(table)  # Write the table rows to the CSV
                        writer.writerow([])  # Write an empty row between tables for readability

    print(f"Tables extracted and saved to {output_csv_path}")

# Example usage
input_pdf = "yellow.pdf"
output_csv = "extracted_tables_with_spaces.csv"
extract_tables_to_csv(input_pdf, output_csv)
