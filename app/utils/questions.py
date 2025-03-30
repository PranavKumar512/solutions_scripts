import pandas as pd
import zipfile
import os
import asyncio
import re
from typing import Optional

from app.utils.GA_1 import *
# =============== Main Resolver Function ===============

# ...existing imports...

# =============== Main Resolver Function ===============

async def solve_question(question: str, file_path: Optional[str] = None) -> dict:
    """
    Asynchronous function to solve the given question by using match-case.
    Returns a dictionary with {"answer": answer}.
    """
    print("Processing the question...")

    # Simulate a delay for testing async behavior
    await asyncio.sleep(2)

    # Match-case to handle different questions
    match question:
        case "Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the \"answer\" column of the CSV file?":
            answer = await handle_zip_question(file_path)

        case _ if re.search(r"(\d+)\s+and\s+(\d+)", question):
            answer = await handle_sum_question(question)

        case "What are the open files in VS Code?":
            answer = get_vscode_open_files()

        case "Extract the email from the text and send a GET request to https://httpbin.org/get. What is the JSON output?":
            text = "email set to 22f3000690@ds.study.iitm.ac.in"
            answer = automate_task(text)

        case "Run Prettier on a file and calculate its SHA-256 checksum.":
            filepath = "example.md"  # Replace with the actual file path
            answer = run_prettier_and_get_checksum(filepath)

        case "What is the result of the Google Sheets formula?":
            text = "=SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 11, 3), 1, 10))"
            answer = automate_google_sheets_task(text)

        case "What is the result of the Excel formula?":
            text = "=SUM(TAKE(SORTBY({3,7,11,0,14,11,12,6,2,10,8,13,12,7,8,3}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 16))"
            answer = automate_excel_task(text)

        case "How many Wednesdays are there in the date range 1981-03-10 to 2016-11-12?":
            text = "How many Wednesdays are there in the date range 1981-03-10 to 2016-11-12?"
            answer = automate_day_count_task(text)

        case "Sort the JSON array by age and name.":
            text = """[{"name":"Alice","age":66},{"name":"Bob","age":35},{"name":"Charlie","age":7}]"""
            answer = extract_and_sort_json(text)

        case "Convert key-value pairs into JSON and calculate the hash.":
            filepath = "key_value_pairs.txt"  # Replace with the actual file path
            answer = automate_hash_task("Convert to JSON and hash", filepath)

        case "Find the sum of data-value attributes in <div> elements with the foo class.":
            html_content = """<div class="foo" data-value="10"></div><div class="foo" data-value="20"></div>"""
            answer = calculate_sum_of_data_values("Find <div> with foo class", html_content)

        case "Process a ZIP file and sum values for specific symbols.":
            zip_file_path = "data_files.zip"  # Replace with the actual file path
            answer = process_zip_and_sum_values("Process ZIP and sum values", zip_file_path)

        case "Create a GitHub repo and push a JSON file.":
            text = '{"email": "22f3000690@ds.study.iitm.ac.in"}'
            answer = create_github_repo_and_push_interactive(text)

        case "Replace 'IITM' with 'IIT Madras' in files and calculate the checksum.":
            zip_file_path = "replace_files.zip"  # Replace with the actual file path
            answer = process_zip_and_replace_text("Replace IITM with IIT Madras", zip_file_path)

        case "Calculate the total size of files modified on or after a specific date.":
            zip_file_path = "list_files.zip"  # Replace with the actual file path
            answer = process_zip_and_calculate_size("Calculate total size", zip_file_path)

        case "Rename files by replacing digits and calculate the checksum.":
            zip_file_path = "rename_files.zip"  # Replace with the actual file path
            answer = process_zip_and_rename_files("Rename files and calculate checksum", zip_file_path)

        case "Compare two files and count differing lines.":
            zip_file_path = "/home/pranav/solutions_scripts/file/compare_files.zip"  # Replace with the actual file path
            answer = process_zip_and_compare_files("Compare files", zip_file_path)

        case "Calculate total sales for 'Gold' ticket type.":
            text = "Calculate total sales for Gold ticket type."
            answer = calculate_total_sales(text)

        case _:
            answer = "Question not recognized."

    # ✅ Return only the answer in the specified format
    return {"answer": answer}


# =============== Question Handlers ===============

async def handle_zip_question(file_path: Optional[str] = None) -> str:
    """
    Handles the ZIP extraction and CSV reading question.
    """
    if file_path and zipfile.is_zipfile(file_path):
        extract_path = "file/extracted"
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Find the CSV file
        csv_file = None
        for root, _, files in os.walk(extract_path):
            for file in files:
                if file.endswith(".csv"):
                    csv_file = os.path.join(root, file)
                    break

        if csv_file:
            df = pd.read_csv(csv_file)
            if "answer" in df.columns:
                answer = df["answer"].iloc[0]
                return str(answer)
            else:
                return "No 'answer' column found in CSV."
        else:
            return "No CSV file found in the ZIP."
    
    return "Invalid or missing ZIP file."


async def handle_sum_question(question: str) -> str:
    """
    Handles the sum calculation question.
    """
    sum_pattern = re.compile(r"(\d+)\s+and\s+(\d+)")
    match = sum_pattern.search(question)

    if match:
        num1, num2 = float(match.group(1)), float(match.group(2))
        result = calculate_sum(num1, num2)
        return f"The sum of {num1} and {num2} is {result}"
    
    return "Invalid sum question format."


# =============== Utility Functions ===============

def calculate_sum(a: float, b: float) -> float:
    """
    Function to calculate the sum of two numbers.
    """
    return a + b
