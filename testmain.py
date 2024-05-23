import streamlit as st
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

    # Perform OCR on the uploaded image
    with st.spinner('Performing OCR...'):
        result = reader.readtext(image)

    # Display OCR result
    st.subheader('OCR Result:')
    for detection in result:
        st.write(detection[1])
