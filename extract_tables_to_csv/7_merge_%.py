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

def merge_columns(table, merge_instructions, delete_columns):
    """
    Merge columns based on the provided instructions. Each item in `merge_instructions` is a tuple
    containing the index of the column to merge and the index of the column to merge it with.
    Columns listed in `delete_columns` will be deleted after merging.
    """
    merged_table = []
    
    for row in table:
        merged_row = []
        i = 0
        while i < len(row):
            if i in merge_instructions:
                # Handle None values and concatenate the two columns safely
                col1 = row[i] if row[i] is not None else ""
                merge_with = merge_instructions[i]
                col2 = row[merge_with] if row[merge_with] is not None else ""
                merged_value = f"{col1} {col2}".strip()
                merged_row.append(merged_value)
                i += 1 if merge_with == i else 2  # Skip the next column if merging with it
            else:
                if i not in delete_columns:
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
                        merge_instructions = {}
                        delete_columns = set()
                        
                        # Handle "$" columns: merge with the next column
                        for i, column in enumerate(table_transposed):
                            if any("$" in str(item) for item in column):
                                merge_instructions[i] = i + 1 if i + 1 < len(table_transposed) else i

                        # Handle "%" columns: apply the 1% vs 2%+ logic
                        for i, column in enumerate(table_transposed):
                            percent_count = sum(1 for item in column if "%" in str(item))
                            if percent_count == 1:
                                # If there is exactly 1 "%", merge with the next column
                                merge_instructions[i] = i + 1 if i + 1 < len(table_transposed) else i
                            elif percent_count >= 2 and i > 0:
                                # If there are 2 or more "%", merge the previous column with the current column
                                merge_instructions[i - 1] = i
                                delete_columns.add(i)  # Mark the current column for deletion after merging

                        # Transpose back to rows
                        cleaned_table = list(zip(*table_transposed))
                        
                        # Merge columns based on the merge_instructions and delete columns after merging
                        if merge_instructions:
                            cleaned_table = merge_columns(cleaned_table, merge_instructions, delete_columns)

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
output_csv = "extracted_tables_percent.csv"
extract_tables_to_csv(input_pdf, output_csv)
