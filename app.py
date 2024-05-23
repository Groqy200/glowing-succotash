import streamlit as st
from PIL import Image
import easyocr
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
import fitz  # PyMuPDF

# Set up EasyOCR and Hugging Face model
easyocr_reader = easyocr.Reader(['en'])
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

# Function to extract text using EasyOCR
def extract_text_easyocr(image):
    results = easyocr_reader.readtext(image)
    text = "\n".join([result[1] for result in results])
    return text

# Function to extract text using Hugging Face model
def extract_text_hf(image):
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

# Function to convert PDF to images
def pdf_to_images(pdf_file):
    doc = fitz.open(pdf_file)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

# Streamlit app
st.title("OCR Web Tool")
st.write("Extract text from images and PDFs, including handwritten notes, using EasyOCR and a Hugging Face model.")

uploaded_file = st.file_uploader("Choose an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        images = pdf_to_images(uploaded_file)
        for i, image in enumerate(images):
            st.image(image, caption=f'Page {i+1}', use_column_width=True)

            st.write(f"Extracted Text from Page {i+1}:")

            # EasyOCR extraction
            st.subheader(f"EasyOCR Output (Page {i+1})")
            easyocr_text = extract_text_easyocr(image)
            st.text(easyocr_text)

            # Hugging Face model extraction
            st.subheader(f"Hugging Face Model Output (Page {i+1})")
            hf_text = extract_text_hf(image)
            st.text(hf_text)
    else:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        st.write("Extracted Text:")

        # EasyOCR extraction
        st.subheader("EasyOCR Output")
        easyocr_text = extract_text_easyocr(image)
        st.text(easyocr_text)

        # Hugging Face model extraction
        st.subheader("Hugging Face Model Output")
        hf_text = extract_text_hf(image)
        st.text(hf_text)
