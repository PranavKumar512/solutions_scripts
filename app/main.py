from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import os
from questions import solve_question

app = FastAPI()

# Ensure the "file" directory exists
os.makedirs("file", exist_ok=True)

@app.post("/api/answers")
async def upload_file(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    file_location = None

    if file:
        file_location = f"file/{file.filename}"

        # ✅ Save the file asynchronously
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        print(f"Saved File: {file_location} ({len(content)} bytes)")

    # ✅ Call `solve_question()` properly
    if callable(solve_question):  
        # Check if the function is sync or async
        if hasattr(solve_question, '__await__'):  
            result = await solve_question(question, file_location)
        else:
            result = solve_question(question, file_location)
    else:
        return {"error": "Invalid solve_question function"}

    # ✅ Return only the answer in JSON format
    return result
