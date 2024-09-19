import pdfplumber
import camelot
import tabula
import pandas as pd
import os

def extract_table_with_pdfplumber(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    return tables

def extract_table_with_camelot(pdf_path):
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor='stream', strip_text='\n')
        return [table.df for table in tables]
    except Exception as e:
        print(f"Error extracting with Camelot: {e}")
        return []

def extract_table_with_tabula(pdf_path):
    try:
        tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
        return tables
    except Exception as e:
        print(f"Error extracting with Tabula: {e}")
        return []

def clean_tables(tables):
    cleaned_tables = []
    for table in tables:
        df = pd.DataFrame(table)
        # Remove any rows or columns containing only percent signs or irrelevant data
        df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how='all')
        df = df.loc[:, (df != '').any(axis=0)]  # Remove empty columns
        # Optionally remove columns that only contain percentages
        df = df.loc[:, ~(df.applymap(lambda x: isinstance(x, str) and '%' in x).all())]
        cleaned_tables.append(df)
    return cleaned_tables

def extract_and_clean_tables(pdf_path):
    # Try extraction with pdfplumber
    tables = extract_table_with_pdfplumber(pdf_path)
    if not tables:
        # Fallback to Camelot if pdfplumber fails
        print("No tables found with pdfplumber, trying Camelot...")
        tables = extract_table_with_camelot(pdf_path)
    
    if not tables:
        # Fallback to Tabula if Camelot fails
        print("No tables found with Camelot, trying Tabula...")
        tables = extract_table_with_tabula(pdf_path)

    if not tables:
        print(f"No tables found in {pdf_path} with any method.")
        return []

    # Clean the extracted tables
    cleaned_tables = clean_tables(tables)

    return cleaned_tables

def save_tables_to_csv(cleaned_tables, output_dir, pdf_filename):
    os.makedirs(output_dir, exist_ok=True)
    for i, df in enumerate(cleaned_tables):
        output_path = os.path.join(output_dir, f"{pdf_filename}_table_{i+1}.csv")
        df.to_csv(output_path, index=False)
        print(f"Table {i+1} saved to {output_path}")

def process_pdf(pdf_path, output_dir="output"):
    print(f"Processing {pdf_path}")
    pdf_filename = os.path.basename(pdf_path).replace(".pdf", "")
    cleaned_tables = extract_and_clean_tables(pdf_path)
    
    if cleaned_tables:
        save_tables_to_csv(cleaned_tables, output_dir, pdf_filename)
    else:
        print(f"No valid tables found in {pdf_filename}.")

if __name__ == "__main__":
    # Example PDFs to process (replace these with actual paths)
    pdf_paths = [
        r"D:\Second\scripts\search_terms\EliteKL23.pdf",
        r"D:\Second\scripts\search_terms\g3holdings23.pdf",
        r"D:\Second\scripts\search_terms\Konsberg23.pdf",
        r"D:\Second\scripts\search_terms\yellow.pdf"
    ]

    output_directory = "output_tables"
    
    for pdf_path in pdf_paths:
        process_pdf(pdf_path, output_directory)