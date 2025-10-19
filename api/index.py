from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import re
import os

# Note: Tesseract OCR must be installed on the system for this to work.
# On Debian/Ubuntu: sudo apt-get install tesseract-ocr
# On macOS: brew install tesseract
# On Windows: Download and install from the official Tesseract repository.
# You may also need to configure the path to the Tesseract executable.
# For example:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to Tesseract executable
# This is for Vercel deployment
tesseract_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tesseract', 'bin', 'tesseract'))
print(f"Attempting to set Tesseract command to: {tesseract_path}")
print(f"Does Tesseract path exist? {os.path.exists(tesseract_path)}")
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    # For local development on Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(f"Falling back to Windows Tesseract path: {pytesseract.pytesseract.tesseract_cmd}")


app = FastAPI(
    title="Document Text Extractor",
    description="An API to extract text from images and documents using Tesseract OCR.",
    version="1.0.0",
)

def parse_text_to_json(text):
    data = {}
    lines = text.split('\n')

    # Regex for key-value pairs
    patterns = {
        "slip_number": r"Slip Number\s*(\S+)",
        "date": r"Date\s*(.+)",
        "customer_name": r"Customer Name\s*(.+)",
        "customer_email": r"Customer Email\s*(\S+)",
        "customer_phone": r"Customer Phone\s*(.+)",
        "shipping_address_street": r"Street\s*(.+)",
        "shipping_address_city": r"City\s*(.+)",
        "shipping_address_state": r"State\s*(.+)",
        "shipping_address_zip": r"Zip Code\s*(\d+)",
        "subtotal": r"Subtotal\s*(\d+\.\d+)",
        "tax": r"Tax\s*\((\d+)%\)\s*(\d+\.\d+)",
        "total": r"Total\s*(\d+\.\d+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if key == "tax":
                data["tax_percentage"] = match.group(1)
                data["tax_amount"] = match.group(2)
            else:
                data[key] = match.group(1).strip()

    # Items table parsing
    items = []
    item_section = False
    header_found = False
    for line in lines:
        if "Product Name" in line and "Quantity" in line:
            header_found = True
            continue
        if "Subtotal" in line:
            item_section = False
            break
        if header_found and line.strip():
            # This regex is designed to be more robust to variations in spacing
            match = re.match(r'^(.*?)\s+(\d+)\s+([\d\.]+)\s+([\d\.]+)$', line.strip())
            if match:
                product_name, quantity, unit_price, total = match.groups()
                items.append({
                    "product_name": product_name.strip(),
                    "quantity": int(quantity),
                    "unit_price": float(unit_price),
                    "total": float(total)
                })
    data["items"] = items

    return data

@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Welcome to the Document Text Extractor API!"}

@app.post("/extract-text/", tags=["Text Extraction"])
async def extract_text(file: UploadFile = File(...)):
    """
    Extracts text from an uploaded image file.

    - **file**: The image file to process.
    """
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        json_output = parse_text_to_json(text)
        return JSONResponse(content=json_output)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)