import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import tempfile
import fitz  # Import PyMuPDF as fitz

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Define function to extract text from image
def extract_text_from_image(image):
    result = reader.readtext(image)
    text = [detection[1] for detection in result]
    return text

# Streamlit app
st.title("OCR Web App")

# Upload PDF document
uploaded_file = st.file_uploader("Choose a PDF document...", type=["pdf"])

# Process PDF and display text
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Open the PDF using PyMuPDF
    doc = fitz.open(temp_file_path)

    # Assuming a single-page PDF with one image
    page = doc.load_page(0)  # Load the first page
    image_list = page.get_images()

    if image_list:
        xref = image_list[0][0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))

        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Convert PIL Image to NumPy array
        image_np = np.array(image)

        extracted_text = extract_text_from_image(image_np)
        st.write("Extracted Text:")
        st.dataframe(extracted_text, column_config={"text": "Extracted Text"})
    else:
        st.write("No images found in the PDF.")
