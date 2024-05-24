import streamlit as st
import easyocr
import pandas as pd
import cv2
from PIL import Image

def streamlit_progress_hook(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    st.write(f'\rDownloading: {percent}%', end='')
    st.progress(percent / 100)


# Initialize the EasyOCR reader with custom progress hook
reader = easyocr.Reader(['en'], download_progress_hook=streamlit_progress_hook)

# Streamlit app
st.title('OCR Web App')

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Perform OCR
    result = reader.readtext(np.array(image))

    # Display the OCR output
    st.write("OCR Output:")
    for res in result:
        st.write(res[1])

    # Convert the OCR output to a DataFrame
    df = pd.DataFrame(result, columns=['Text'])

    # Download the OCR output as a .csv file
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='ocr_output.csv',
        mime='text/csv',
    )
