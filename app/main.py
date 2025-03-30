from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import os
from questions import solve_question

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

    result = await solve_question(question, file_location)
    
    return result

# ASGI handler for Vercel
def handler(req, res):
    from mangum import Mangum
    asgi_handler = Mangum(app)
    return asgi_handler(req, res)
