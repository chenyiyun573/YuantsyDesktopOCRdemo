import json
import requests
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from ocr_call import get_ocr_results  # Import the function from your ocr_api.py

# URL of the PNG screenshot
image_url = "http://mq.yuantsy.com:4001/Timeline/20240525_1731_BJT_757694_example.png"

# Download the image
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
image_width, image_height = image.size

# Call the function to get OCR results
ocr_data = get_ocr_results(image_url)
ocr_result = json.loads(ocr_data)

# Create a PDF canvas with the same dimensions as the image
c = canvas.Canvas("output.pdf", pagesize=(image_width, image_height))

# Extract TextDetections if they exist in the response
if 'TextDetections' in ocr_result:
    for item in ocr_result['TextDetections']:
        text = item['DetectedText']
        x = item['ItemPolygon']['X']
        y = image_height - item['ItemPolygon']['Y'] - item['ItemPolygon']['Height']  # Adjust Y coordinate
        width = item['ItemPolygon']['Width']
        height = item['ItemPolygon']['Height']

        # Draw rectangle around text
        c.rect(x, y, width, height, stroke=1, fill=0)

        # Draw text within the rectangle
        c.drawString(x + 2, y + height - 12, text)  # Adjust text position within rectangle

# Save the PDF
c.save()
