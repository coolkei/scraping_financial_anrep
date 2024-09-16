import pdfplumber
import csv

def extract_tables_to_csv(input_pdf_path, output_csv_path):
    with pdfplumber.open(input_pdf_path) as pdf:
        all_tables = []  # Store all the extracted tables in this list

        for page_num, page in enumerate(pdf.pages):
            # Extract tables from each page
            tables = page.extract_tables()

            if tables:
                for table in tables:
                    all_tables.extend(table)  # Append the table rows to the list

    # Now, save the tables to a CSV file
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(all_tables)

    print(f"Tables extracted and saved to {output_csv_path}")

# Example usage
input_pdf = "yellow.pdf"
output_csv = "extracted_tables.csv"
extract_tables_to_csv(input_pdf, output_csv)
