import streamlit as st
import easyocr
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False, platform='tf')

st.title("OCR Web App")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Perform OCR
    ocr_result = reader.readtext(image)

    # Display OCR output
    st.write("---")
    st.subheader("OCR Output")
    for line in ocr_result:
        text, _ = line
        st.write(text)
