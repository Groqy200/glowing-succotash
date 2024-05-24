import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import tempfile

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

    # Extract images from PDF (replace with actual PDF image extraction)
    # Placeholder: Assuming a single-page PDF with one image
    image = Image.open(temp_file_path)  

    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert PIL Image to NumPy array
    image_np = np.array(image)

    extracted_text = extract_text_from_image(image_np)
    st.write("Extracted Text:")
    st.dataframe(extracted_text, column_config={"text": "Extracted Text"})
