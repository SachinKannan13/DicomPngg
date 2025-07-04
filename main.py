from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pydicom
from PIL import Image
import numpy as np
import os
import uuid

app = FastAPI()

@app.post("/convert/")
async def convert_dicom(file: UploadFile = File(...)):
    # Save uploaded DICOM temporarily
    temp_filename = f"temp_{uuid.uuid4()}.dcm"
    with open(temp_filename, "wb") as f:
        content = await file.read()
        f.write(content)

    # Read and process DICOM
    dicom_data = pydicom.dcmread(temp_filename)
    pixel_array = dicom_data.pixel_array
    image = Image.fromarray((pixel_array / pixel_array.max() * 255).astype(np.uint8))
    
    png_filename = temp_filename.replace(".dcm", ".png")
    image.save(png_filename)

    # Clean up original
    os.remove(temp_filename)

    return FileResponse(png_filename, media_type="image/png", filename="converted.png")
