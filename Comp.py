import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import tempfile
import fitz
import io

# Initialize EasyOCR reader
reader = easyocr.Reader(['en']) 

# Define function to extract text from image (with potential optimizations)
def extract_text_from_image(image):
    # Convert to grayscale if image mode is not already 'L' (grayscale)
    if image.mode != 'L':
        image = image.convert('L')

    result = reader.readtext(np.array(image))  # Directly convert to NumPy array
    text = [detection[1] for detection in result]
    return text

# Streamlit app
st.title("OCR Web App")

# Upload file (PDF or image)
uploaded_file = st.file_uploader("Choose a PDF document or an image file...", 
                                type=["pdf", "jpg", "jpeg", "png"])

# Process file based on type
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # Handle PDF
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Open the PDF using PyMuPDF
        doc = fitz.open(temp_file_path)
        
        # Process all pages in the PDF
        for page_num in range(doc.page_count):
            page = doc[page_num]
            image_list = page.get_images()

            if image_list:
                for img in image_list:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))

                    # Resize image (adjust max_width as needed)
                    max_width = 800
                    if image.width > max_width:
                        width_percent = (max_width / float(image.width))
                        height = int((float(image.height) * float(width_percent)))
                        image = image.resize((max_width, height), Image.Resampling.LANCZOS)

                    st.image(image, caption=f'Page {page_num+1} - Image', use_column_width=True)

                    extracted_text = extract_text_from_image(image)
                    st.write(f"Extracted Text from Page {page_num+1} - Image:")
                    st.dataframe(extracted_text, column_config={"text": "Extracted Text"})
            else:
                st.write(f"No images found on page {page_num+1} of the PDF.")

    else:
        # Handle image
        image = Image.open(uploaded_file)

        # Resize image (adjust max_width as needed)
        max_width = 800
        if image.width > max_width:
            width_percent = (max_width / float(image.width))
            height = int((float(image.height) * float(width_percent)))
            image = image.resize((max_width, height), Image.Resampling.LANCZOS)

        st.image(image, caption='Uploaded Image', use_column_width=True)

        extracted_text = extract_text_from_image(image)
        st.write("Extracted Text:")
        st.dataframe(extracted_text, column_config={"text": "Extracted Text"})
