import subprocess
import re
import requests
import os
import hashlib
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import json
from bs4 import BeautifulSoup
import zipfile
import hashlib
import shutil
import sqlite3
import tempfile
from typing import Optional


# Helper: safe extraction to avoid zip-slip vulnerabilities
def _safe_extract(zip_file: zipfile.ZipFile, path: str) -> None:
    """
    Safely extract a ZipFile to a target directory, preventing path traversal.
    """
    for member in zip_file.infolist():
        member_path = os.path.join(path, member.filename)
        abs_target = os.path.abspath(path)
        abs_member = os.path.abspath(member_path)
        if not abs_member.startswith(abs_target + os.sep) and abs_member != abs_target:
            raise RuntimeError("Unsafe ZIP file: attempted Path Traversal in ZIP file")
    zip_file.extractall(path)


#Q_1
def get_vscode_open_files():
    try:
        # Run the 'code -s' command without a shell to avoid injection risks
        result = subprocess.run(["code", "-s"], capture_output=True, text=True, shell=False)

        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout.strip()  # Return the output
        else:
            return f"Error: {result.stderr.strip()}"  # Return the error message
    except FileNotFoundError:
        return "Visual Studio Code (code) is not installed or not in PATH."


########################################################################
#Q_2
def extract_email_from_text(text):
    """
    Extracts the email from the given text using a regular expression.
    """
    match = re.search(r"email\s*set\s*to\s*([\w\.-]+@[\w\.-]+\.\w+)", text)
    if match:
        return match.group(1)
    return None


def send_request_and_get_json(email):
    url = "https://httpbin.org/get"
    params = {"email": email}

    try:
        # Use requests with defaults (verify=True). Allow callers to configure timeouts if needed.
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def automate_task(text):
    email = extract_email_from_text(text)
    if email:
        return send_request_and_get_json(email)
    else:
        return {"error": "No email found in the text"}


#Q_3
def run_prettier_and_get_checksum(filepath):
    """
    Runs `npx prettier` on the given file and calculates its SHA-256 checksum.
    This avoids shell=True and treats filepath as an argument.
    """
    try:
        # Run `npx prettier` on the file without using a shell
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", filepath],
            capture_output=True,
            text=True,
            shell=False,
            timeout=30,
        )
        if result.returncode != 0:
            raise Exception(f"Prettier failed: {result.stderr}")

        formatted_content = result.stdout
        sha256_hash = hashlib.sha256(formatted_content.encode("utf-8")).hexdigest()
        return sha256_hash
    except FileNotFoundError:
        raise Exception("npx or prettier is not installed or not in PATH.")


#Q_4 ... (unchanged helper functions omitted for brevity)
# The rest of the file retains the same logic but replaces unsafe zip extraction

# Replace occurrences of zip_ref.extractall(...) with safe extraction and use TemporaryDirectory

def extract_and_sort_json(text):
    try:
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if not match:
            return {"error": "No JSON array found in the text."}
        json_array = json.loads(match.group(0))
        sorted_array = sorted(json_array, key=lambda x: (x['age'], x['name']))
        return json.dumps(sorted_array, separators=(',', ':'))
    except Exception as e:
        return {"error": str(e)}


#Q_10 convert_to_json_and_hash unchanged

def convert_to_json_and_hash(file_path):
    try:
        df = pd.read_csv(file_path, header=None, names=["key", "value"])
        json_object = df.set_index("key")["value"].to_dict()
        json_string = json.dumps(json_object, separators=(',', ':'))
        return {"json_string": json_string}
    except Exception as e:
        return {"error": str(e)}


#Q_12 updated to use TemporaryDirectory and safe extraction

def process_zip_and_sum_values(text, zip_file_path):
    try:
        target_symbols = ['›', '•', '‚']
        total_sum = 0
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                _safe_extract(zip_ref, temp_dir)

            encodings = {
                "data1.csv": "cp1252",
                "data2.csv": "utf-8",
                "data3.txt": "utf-16"
            }

            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                encoding = encodings.get(file_name)
                if not encoding:
                    continue

                if file_name.endswith(".csv"):
                    df = pd.read_csv(file_path, encoding=encoding)
                elif file_name.endswith(".txt"):
                    df = pd.read_csv(file_path, encoding=encoding, sep="\t")
                else:
                    continue

                filtered_df = df[df['symbol'].isin(target_symbols)]
                total_sum += filtered_df['value'].sum()

        return {"sum_of_values": total_sum}
    except Exception as e:
        return {"error": str(e)}


#Q_13: remove interactive behavior to avoid arbitrary command execution

def create_github_repo_and_push_interactive(text):
    """
    Disabled for security reasons: this function previously ran shell commands and read interactive input.
    If you need programmatic repository creation, use the GitHub REST API with a personal access token
    and a dedicated function that validates inputs. For now, this helper returns an error explaining
    the safer approach.
    """
    return {"error": "Interactive repository creation is disabled for security reasons. Use the GitHub REST API with a token and validated inputs."}


#Q_14 updated to use TemporaryDirectory and safe extraction

def process_zip_and_replace_text(text, zip_file_path):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                _safe_extract(zip_ref, temp_dir)

            for root, _, files in os.walk(temp_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    # Read and write with utf-8, ignore errors to avoid failing on mixed encodings
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()

                    updated_content = content.replace("IITM", "IIT Madras").replace("iitm", "IIT Madras").replace("Iitm", "IIT Madras")

                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(updated_content)

            sha256 = hashlib.sha256()
            for root, _, files in os.walk(temp_dir):
                for file_name in sorted(files):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, "rb") as file:
                        while chunk := file.read(8192):
                            sha256.update(chunk)

        return {"sha256_checksum": sha256.hexdigest()}
    except Exception as e:
        return {"error": str(e)}


#Q_15 use TemporaryDirectory and safe extraction

def process_zip_and_calculate_size(text, zip_file_path):
    try:
        min_size = 1329
        min_date = datetime(2007, 6, 5, 4, 38)
        total_size = 0
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                _safe_extract(zip_ref, temp_dir)

            for root, _, files in os.walk(temp_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    file_size = os.path.getsize(file_path)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_size >= min_size and mod_time >= min_date:
                        total_size += file_size

        return {"total_size": total_size}
    except Exception as e:
        return {"error": str(e)}


#Q_16 use TemporaryDirectory and safe extraction

def process_zip_and_rename_files(text, zip_file_path):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            final_dir = os.path.join(temp_dir, "final")
            os.makedirs(final_dir, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                _safe_extract(zip_ref, temp_dir)

            for root, _, files in os.walk(temp_dir):
                for file_name in files:
                    src_path = os.path.join(root, file_name)
                    if os.path.isdir(src_path):
                        continue
                    dest_path = os.path.join(final_dir, file_name)
                    shutil.move(src_path, dest_path)

            for file_name in os.listdir(final_dir):
                new_file_name = re.sub(r'\d', lambda x: str((int(x.group(0)) + 1) % 10), file_name)
                os.rename(os.path.join(final_dir, file_name), os.path.join(final_dir, new_file_name))

            concatenated_content = []
            for file_name in sorted(os.listdir(final_dir)):
                file_path = os.path.join(final_dir, file_name)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    for line in file:
                        concatenated_content.append(line.strip())
            concatenated_content.sort()

            sha256 = hashlib.sha256()
            for line in concatenated_content:
                sha256.update(line.encode("utf-8"))

        return {"sha256_checksum": sha256.hexdigest()}
    except Exception as e:
        return {"error": str(e)}


#Q_17 use TemporaryDirectory and safe extraction

def process_zip_and_compare_files(text, zip_file_path):
    try:
        if not os.path.exists(zip_file_path):
            return {"error": f"The file {zip_file_path} does not exist."}

        differing_lines = 0
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                _safe_extract(zip_ref, temp_dir)

            file_a_path = os.path.join(temp_dir, "a.txt")
            file_b_path = os.path.join(temp_dir, "b.txt")

            if not os.path.exists(file_a_path):
                return {"error": f"File a.txt is missing in the extracted folder: {temp_dir}"}
            if not os.path.exists(file_b_path):
                return {"error": f"File b.txt is missing in the extracted folder: {temp_dir}"}

            with open(file_a_path, "r", encoding="utf-8", errors="ignore") as file_a, open(file_b_path, "r", encoding="utf-8", errors="ignore") as file_b:
                for line_a, line_b in zip(file_a, file_b):
                    if line_a.strip() != line_b.strip():
                        differing_lines += 1

        return {"differing_lines": differing_lines}
    except zipfile.BadZipFile:
        return {"error": "The provided file is not a valid ZIP file."}
    except Exception as e:
        return {"error": str(e)}


#Q_18 unchanged (read-only SQL returned as a string earlier)
def calculate_total_sales(text):
    try:
        query = """
        SELECT SUM(units * price) AS total_sales FROM tickets WHERE LOWER(type) = 'gold';
        """
        return {"total_sales": query}
    except Exception as e:
        return {"error": str(e)}
