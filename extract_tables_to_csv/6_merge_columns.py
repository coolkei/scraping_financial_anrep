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

def merge_columns(table, dollar_column_indices):
    """
    Merge the columns containing the dollar sign with the next column.
    """
    merged_table = []
    
    for row in table:
        merged_row = []
        i = 0
        while i < len(row):
            if i in dollar_column_indices and i + 1 < len(row):
                # Handle None values and concatenate the two columns safely
                col1 = row[i] if row[i] is not None else ""
                col2 = row[i+1] if row[i+1] is not None else ""
                merged_value = f"{col1} {col2}".strip()
                merged_row.append(merged_value)
                i += 2  # Skip the next column since it has been merged
            else:
                # Append the other columns as they are
                merged_row.append(row[i])
                i += 1
        merged_table.append(merged_row)
    
    return merged_table

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
                        
                        # Look for all columns with a "$" symbol
                        dollar_column_indices = []
                        for i, column in enumerate(table_transposed):
                            if any("$" in str(item) for item in column):
                                dollar_column_indices.append(i)

                        # If columns with "$" are found, merge them with the next column
                        if dollar_column_indices:
                            # Transpose back to rows
                            cleaned_table = list(zip(*table_transposed))
                            # Merge all identified columns with their next column
                            cleaned_table = merge_columns(cleaned_table, dollar_column_indices)

                        # Transpose back to columns to filter out empty columns
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
output_csv = "extracted_tables_ox.csv"
extract_tables_to_csv(input_pdf, output_csv)
