# Document Text Extractor

An API to extract text and structured data from images and documents using Tesseract OCR.

## Features

- Extracts raw text from images.
- Parses extracted text to a structured JSON format.
- Deploys easily to Vercel.

## Local Development

### Prerequisites

- Python 3.7+
- Tesseract OCR

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KolipakaRamesh/DocumentTextExtractor.git
    cd DocumentTextExtractor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Tesseract:**
    Make sure Tesseract OCR is installed and accessible. If it's not in your system's PATH, you may need to update the path in `api/index.py`.

4.  **Run the application:**
    ```bash
    python -m uvicorn api.index:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

## API Endpoint

### `POST /extract-text/`

Extracts text from an uploaded image file and returns it in a structured JSON format.

-   **Request:** `multipart/form-data` with a `file` field containing the image.
-   **Response:** A JSON object with the extracted data.

**Example Response:**
```json
{
  "slip_number": "S-2021-001",
  "date": "May 25, 2021",
  "customer_name": "John Smith",
  "customer_email": "phn.smith@example.con",
  "customer_phone": "(123) 456-7890",
  "shipping_address_street": "123 Main St",
  "shipping_address_city": "Anytown",
  "shipping_address_state": "California",
  "shipping_address_zip": "12345",
  "subtotal": "98.9",
  "tax_percentage": "7",
  "tax_amount": "6.92",
  "total": "105.82",
  "items": [
    {
      "product_name": "Product A",
      "quantity": 2,
      "unit_price": 10.99,
      "total": 21.98
    },
    {
      "product_name": "Product B",
      "quantity": 1,
      "unit_price": 24.99,
      "total": 24.99
    },
    {
      "product_name": "Product C",
      "quantity": 3,
      "unit_price": 5.99,
      "total": 17.97
    },
    {
      "product_name": "Product D",
      "quantity": 4,
      "unit_price": 8.49,
      "total": 33.96
    }
  ]
}
```

## Deployment

This project is configured for deployment on Vercel. Simply connect your GitHub repository to a new Vercel project. The `vercel.json` and `build.sh` files will handle the deployment and Tesseract installation automatically.
