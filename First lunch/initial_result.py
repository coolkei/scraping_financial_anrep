import re
import PyPDF2
import pandas as pd

search_terms = {
    "Revenue / Turnover / Sales": [
        "Revenue",
        "Turnover",
        "Sales"
    ],
    "Cost of Sales / Operating Costs": [
        "Cost of Sales",
        "Operating Costs"
    ],
    "Raw materials, subcontracts and other bought-in items": [
        "Raw materials, subcontracts and other bought-in items"
    ],
    "Administrative Expenses": [
        "Administrative Expenses"
    ],
    "Other Operating Charges / Sales & Distribution Expenses": [
        "Other Operating Charges",
        "Sales & Distribution Expenses"
    ],
    "EBITDA": [
        "EBITDA"
    ],
    "Net Profit (Before Tax) / Operating Result / Operating Profit": [
        "Net Profit (Before Tax)",
        "Operating Result",
        "Operating Profit"
    ],
    "Net Interest Cost / Finance Expense": [
        "Net Interest Cost",
        "Finance Expense"
    ],
    "Tax": [
        "Tax"
    ],
    "Net Profit (After Tax)": [
        "Net Profit (After Tax)"
    ],
    "Earnings per Share (Diluted)": [
        "Earnings per Share (Diluted)"
    ],
    "Balance Sheet / Consolidated Balance Sheet": [
        "Balance Sheet",
        "Consolidated Balance Sheet"
    ],
    "Fixed Assets / Non-Current Assets": [
        "Fixed Assets",
        "Non-Current Assets"
    ],
    "Intangible Assets": [
        "Intangible Assets"
    ],
    "Goodwill": [
        "Goodwill"
    ],
    "Tangible Assets": [
        "Tangible Assets"
    ],
    "Property, Plant and Equipment": [
        "Property, Plant and Equipment"
    ],
    "Fixed Assets / Non-Current Assets (Total)": [
        "Fixed Assets",
        "Non-Current Assets (Total)"
    ],
    "Current Assets": [
        "Current Assets"
    ],
    "Inventory / Stock / Inventories": [
        "Inventory",
        "Stock",
        "Inventories"
    ],
    "Trade Receivables / Trade and other Receivables / Debtors: amounts falling due within one year": [
        "Trade Receivables",
        "Trade and other Receivables",
        "Debtors: amounts falling due within one year"
    ],
    "Cash and cash equivalents / Cash at Bank and in Hand": [
        "Cash and cash equivalents",
        "Cash at Bank and in Hand"
    ],
    "Current Assets (Total)": [
        "Current Assets (Total)"
    ],
    "Total Assets (Total)": [
        "Total Assets (Total)"
    ],
    "Current Liabilities": [
        "Current Liabilities"
    ],
    "Borrowings / Loans and Overdrafts": [
        "Borrowings",
        "Loans and Overdrafts"
    ],
    "Trade Payables / Creditors: amounts falling due within one year": [
        "Trade Payables",
        "Creditors: amounts falling due within one year"
    ],
    "Income Tax Payable / Current Tax": [
        "Income Tax Payable",
        "Current Tax"
    ],
    "Current Liabilities (Total)": [
        "Current Liabilities (Total)"
    ],
    "Long-Term Liabilities / Non-Current Liabilities": [
        "Long-Term Liabilities",
        "Non-Current Liabilities"
    ],
    "Loans / Creditors: amounts falling due after more than one year / Long-Term Debt / Long-Term Loans": [
        "Loans",
        "Creditors: amounts falling due after more than one year",
        "Long-Term Debt",
        "Long-Term Loans"
    ],
    "Pension Surplus / (Deficit) / Retirement Benefit Obligations": [
        "Pension Surplus",
        "(Deficit)",
        "Retirement Benefit Obligations"
    ],
    "Other Liabilities": [
        "Other Liabilities"
    ],
    "Provisions": [
        "Provisions"
    ],
    "Long-Term Liabilities / Non-Current Liabilities (Total)": [
        "Long-Term Liabilities",
        "Non-Current Liabilities (Total)"
    ],
    "Total Liabilities (Total)": [
        "Total Liabilities (Total)"
    ],
    "Capital & Reserves": [
        "Capital & Reserves"
    ],
    "Retained Earnings / Profit and loss account": [
        "Retained Earnings",
        "Profit and loss account"
    ],
    "Total Shareholders Funds / Net Assets / Net Book Value / Total Equity": [
        "Total Shareholders Funds",
        "Net Assets",
        "Net Book Value",
        "Total Equity"
    ],
    "Cash Flow Statement": [
        "Cash Flow Statement"
    ],
    "Cash Flow from Operating Activities": [
        "Cash Flow from Operating Activities"
    ],
    "Profit / Loss for the Year": [
        "Profit",
        "Loss for the Year"
    ],
    "Depreciation, Amortisation & Impairment": [
        "Depreciation",
        "Amortisation",
        "Impairment"
    ],
    "Movements in Provisions": [
        "Movements in Provisions"
    ],
    "Net Cash Flow from Operating Activities (Total)": [
        "Net Cash Flow from Operating Activities (Total)"
    ],
    "Cash Flow from Investing Activities": [
        "Cash Flow from Investing Activities"
    ],
    "Purchase of Property, Plant and Equipment, and investment property": [
        "Purchase of Property",
        "Plant and Equipment",
        "investment property"
    ],
    "Net Cash used in Investing Activities (Total)": [
        "Net Cash used in Investing Activities (Total)"
    ],
    "Cash Flow from Financing Activities": [
        "Cash Flow from Financing Activities"
    ],
    "Purchase of own Shares + Purchase of Treasury Shares": [
        "Purchase of own Shares",
        "Purchase of Treasury Shares"
    ],
    "Dividends Paid": [
        "Dividends Paid"
    ],
    "Cash Flow from Financing Activities (Total)": [
        "Cash Flow from Financing Activities (Total)"
    ],
    "Cash & Cash Equivalents": [
        "Cash & Cash Equivalents"
    ],
    "Annual Report & Notes": [
        "Annual Report & Notes"
    ],
    "Average Share Price": [
        "Average Share Price"
    ],
    "# Shares Outstanding": [
        "# Shares Outstanding"
    ],
    "# Treasury Shares": [
        "# Treasury Shares"
    ],
    "Dividend per Share": [
        "Dividend per Share"
    ],
    "Administration": [
        "Administration"
    ],
    "Operations": [
        "Operations"
    ],
    "# Employees": [
        "# Employees"
    ],
    "Wages and Salaries": [
        "Wages and Salaries"
    ],
    "Employee Costs / Staff Costs": [
        "Employee Costs",
        "Staff Costs"
    ],
    "Wages and Salaries per Head": [
        "Wages and Salaries per Head"
    ],
    "Revenue / Turnover / Sales per Head": [
        "Revenue",
        "Turnover",
        "Sales per Head"
    ],
    "Research & Development Expenditure (Combined)": [
        "Research & Development Expenditure (Combined)"
    ],
    "Depreciation / Amortisation / Right-of-use Assets": [
        "Depreciation",
        "Amortisation",
        "Right-of-use Assets"
    ],
    "Leases / Rentals": [
        "Leases",
        "Rentals"
    ]
}

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = ""
    for page_num in range(len(pdf_reader.pages)):
        extracted_text += pdf_reader.pages[page_num].extract_text()
    return extracted_text

def find_terms_and_values(text, search_terms):
    extracted_data = {}
    for term, variations in search_terms.items():
        for variation in variations:
            pattern = re.compile(rf"{variation}\s*[:\-]?\s*(\d[\d,\.]*)", re.IGNORECASE)
            match = pattern.search(text)
            if match:
                extracted_data[term] = match.group(1)
                break
    return extracted_data

def process_pdf_to_excel(pdf_path, excel_output):
    with open(pdf_path, 'rb') as pdf_file:
        text = extract_text_from_pdf(pdf_file)
    
    extracted_data = find_terms_and_values(text, search_terms)

    df = pd.DataFrame(list(extracted_data.items()), columns=["Term", "Value"])

    df.to_excel(excel_output, index=False)
    print(f"Data Successfully extracted and saved to {excel_output}")

pdf_path = "yellow.pdf"
excel_output = "output_data.xlsx"
process_pdf_to_excel(pdf_path, excel_output)