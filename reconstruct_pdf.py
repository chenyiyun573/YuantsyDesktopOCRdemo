import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from ocr_call import get_ocr_results  # Import the function from your ocr_api.py

# Call the function to get OCR results
ocr_data = get_ocr_results(os.getenv("screenshot_url"))
ocr_result = json.loads(ocr_data)

# Create a PDF canvas
c = canvas.Canvas("output.pdf", pagesize=A4)
width, height = A4  # Get page size
print(width, height)

# Extract TextDetections if it exists in the response
if 'TextDetections' in ocr_result:
    for item in ocr_result['TextDetections']:
        text = item['DetectedText']
        x = item['ItemPolygon']['X']
        y = height - item['ItemPolygon']['Y']  # Adjust Y coordinate
        c.drawString(x, y, text)

# Save the PDF
c.save()
