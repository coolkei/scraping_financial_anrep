import pdfplumber
import csv
import re

def clean_item(item):
    # Step 1: Remove "(" if it is followed by only numbers
    if re.match(r"\(\d+", item):
        item = item.replace("(", "")  # Remove the opening parenthesis
    
    # Step 2: If the item is exactly ")", replace it with an empty string
    elif item == ")":
        item = ""  # Replace ")" with an empty string

    # Step 3: If the item is exactly "%)", replace it with an empty string
    elif item == "%)":
        item = ""  # Replace "%)" with an empty string

    # Step 4: Replace ")" followed by unit symbols (%$, &, etc.), leave other cases like "annual(not)" untouched
    else:
        item = re.sub(r"\)([%$&]+)", "", item)  # Remove ")" and valid unit symbols, but leave other cases intact

    return item

def extract_tables_to_csv(input_pdf_path, output_csv_path):
    with pdfplumber.open(input_pdf_path) as pdf:
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            for page_num, page in enumerate(pdf.pages):
                # Extract tables from each page
                tables = page.extract_tables()

                if tables:
                    for table in tables:
                        # Clean and process each item in the table
                        cleaned_table = [
                            [clean_item(item) if item else item for item in row]
                            for row in table
                        ]

                        # Transpose the table to work with columns
                        table_transposed = list(zip(*cleaned_table))
                        
                        # Remove columns where all values are None or empty
                        filtered_columns = [col for col in table_transposed if any(val for val in col if val and val.strip())]
                        
                        # Transpose back to rows
                        filtered_table = list(zip(*filtered_columns)) if filtered_columns else []

                        if filtered_table:
                            writer.writerows(filtered_table)  # Write the filtered table rows to the CSV
                            writer.writerow([])  # Write an empty row between tables for readability

    print(f"Tables extracted and saved to {output_csv_path}")

# Example usage
input_pdf = "D:/Second/scripts/PDFs/Yellow Corporation 2022 Annual Report.pdf"
output_csv = "extracted_tables_cleaned.csv"
extract_tables_to_csv(input_pdf, output_csv)
