import streamlit as st
from PIL import Image
from easyocr import Reader

# Create an EasyOCR reader
reader = Reader(['en'])

# Streamlit app
st.title('OCR Web App')

# Upload image
image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

if image is not None:
    # Display uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert uploaded image to PIL format
    img = Image.open(image)

    # Perform OCR on the uploaded image
    with st.spinner('Performing OCR...'):
        result = reader.readtext(img)

    # Display OCR result
    st.subheader('OCR Result:')
    for detection in result:
        st.write(detection[1])
