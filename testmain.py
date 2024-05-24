import streamlit as st
from PIL import Image
import easyocr
import numpy as np 

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  

# Define function to extract text from image
def extract_text_from_image(image):
    result = reader.readtext(image)
    text = [detection[1] for detection in result] 
    return text

# Streamlit app
st.title("OCR Web App")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Process image and display text
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Convert PIL Image to NumPy array
    image_np = np.array(image) 
    
    extracted_text = extract_text_from_image(image_np) 
    st.write("Extracted Text:")
    st.dataframe(extracted_text, column_config={"text": "Extracted Text"}) 
