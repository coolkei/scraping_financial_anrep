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
                        # Transpose the table to work with columns
                        table_transposed = list(zip(*table))
                        
                        # Remove columns where all values are None or empty
                        filtered_columns = [col for col in table_transposed if any(val for val in col if val and val.strip())]
                        
                        # Transpose back to rows
                        filtered_table = list(zip(*filtered_columns)) if filtered_columns else []

                        if filtered_table:
                            writer.writerows(filtered_table)  # Write the filtered table rows to the CSV
                            writer.writerow([])  # Write an empty row between tables for readability

    print(f"Tables extracted and saved to {output_csv_path}")

# Example usage
input_pdf = "yellow.pdf"
output_csv = "extracted_tables_without_empty_columns.csv"
extract_tables_to_csv(input_pdf, output_csv)
