from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import os
from app.utils.questions import solve_question
from mangum import Mangum

app = FastAPI()

# Ensure the 'file' directory exists
os.makedirs("file", exist_ok=True)

@app.post("/api/answers")
async def upload_file(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    file_location = None
    if file:
        file_location = f"file/{file.filename}"
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

    # Call the solve_question function
    result = solve_question(question, file_location)  # Removed await if sync

    # ✅ Clean up the uploaded file after processing
    if file_location and os.path.exists(file_location):
        os.remove(file_location)

    return result

# ✅ ASGI handler for Vercel
handler = Mangum(app)
