from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from app.utils.questions import solve_question  # Ensure this module exists
from mangum import Mangum

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure 'file' directory exists
os.makedirs("file", exist_ok=True)

@app.get("/")
async def hello():
    return {"message": "Hello from Vercel"}

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

    # Call the solve_question function (Ensure it exists)
    result = solve_question(question, file_location)  

    # Clean up the uploaded file after processing
    if file_location and os.path.exists(file_location):
        os.remove(file_location)

    return result

# ✅ ASGI handler for Vercel
handler = Mangum(app)