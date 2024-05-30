import streamlit as st
import cv2

# Upload image
uploaded_file = st.file_uploader("Upload Invoice Image")

# Preprocess image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

if uploaded_file:
    image = cv2.imread(uploaded_file)
    preprocessed_image = preprocess_image(image)

import pytesseract
from medusa import *

# OCR (Printed Text)
def extract_printed_text(image):
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 11')
    return text

# HTR (Handwritten Text)
def extract_handwritten_text(image):
    medusa = Medusa()
    text = medusa.recognize(image)
    return text

if preprocessed_image:
    printed_text = extract_printed_text(preprocessed_image)
    handwritten_text = extract_handwritten_text(preprocessed_image)

from layoutparser import LayoutParser
from gobi import Gobi

# Extract invoice structure
def extract_structure(image):
    layout_parser = LayoutParser()
    structure = layout_parser.detect(image)
    return structure

# Extract relevant information
def extract_info(structure):
    gobi = Gobi()
    info = gobi.extract(structure, ['date', 'amount', 'vendor'])
    return info

if preprocessed_image:
    structure = extract_structure(preprocessed_image)
    info = extract_info(structure)

import csv

# Generate CSV file
def generate_csv(info):
    with open('invoice_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([info['date'], info['amount'], info['vendor']])

if info:
    generate_csv(info)

st.title("Invoice OCR Web App")
st.write("Upload an invoice image to extract information")

# Display extracted information
if info:
    st.write("Extracted Information:")
    st.write(f"Date: {info['date']}")
    st.write(f"Amount: {info['amount']}")
    st.write(f"Vendor: {info['vendor']}")

    # Download CSV button
    with open('invoice_info.csv', 'rb') as file:
        st.download_button("Download CSV", file, "invoice_info.csv"
