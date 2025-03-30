
# FastAPI Question Solver

A FastAPI-based application that processes various types of questions, including:
- Extracting values from CSV files inside ZIP archives.
- Performing basic arithmetic operations (sum of two numbers).

---

## 🚀 Features

- Asynchronous processing using `asyncio`.
- Supports multipart file uploads.
- Only returns the answer in the format:
```json
{"answer": "The solution to the question."}
```
- Lightweight and fast execution.

---

## 🛠️ Environment Setup

### ✅ **For Linux**

1. **Clone the Repository**
```bash
git clone <repository_url>
cd <repository_name>
```

2. **Install uv (Python environment manager)**  
If you don't have `uv` installed:
```bash
pip install uv
```

3. **Create the Environment**
```bash
uv venv
```

4. **Activate the Environment**
```bash
source .venv/bin/activate
```

5. **Install Dependencies**
```bash
uv pip install -r requirements.txt
```

---

### ✅ **For Windows**

1. **Clone the Repository**
```powershell
git clone <repository_url>
cd <repository_name>
```

2. **Install uv (Python environment manager)**  
If you don't have `uv` installed:
```powershell
pip install uv
```

3. **Create the Environment**
```powershell
uv venv
```

4. **Activate the Environment**
```powershell
.venv\Scripts\activate
```

5. **Install Dependencies**
```powershell
uv pip install -r requirements.txt
```

---

## 🚀 Running the Server

After setting up the environment, run the FastAPI server using:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📤 API Usage

### ✅ **POST Request**
You can send requests using `curl` or Postman.

### **With File Upload**
```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the \"answer\" column of the CSV file?" \
  -F "file=@/path/to/abcd.zip"
```

### **Without File Upload**
```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=What is the sum of 10 and 25?"
```

---

## 🧑‍💻 Example Responses

### **ZIP File Question**
```json
{"answer": "42"}
```

### **Sum Question**
```json
{"answer": "The sum of 10.0 and 25.0 is 35.0"}
```

---

## 📚 Project Structure

```
/file                  # Directory for uploaded files
    └── extracted      # Extracted ZIP content
main.py                 # FastAPI server
questions.py            # Logic to process questions
README.md               # Documentation
requirements.txt        # Dependencies
```

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
