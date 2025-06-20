import streamlit as st
from docx import Document
import pdfplumber
from transformers import BartTokenizer, BartForConditionalGeneration
import torch
import os

# Load model and tokenizer
@st.cache_resource
def load_model():
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
    return model, tokenizer

model, tokenizer = load_model()

# Streamlit UI
st.title("EHCP Report Generator")

uploaded_files = st.file_uploader("Upload one or more EHCP documents (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif file.name.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text.strip()

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"Processing: {file.name}")
        extracted_text = extract_text(file)

        inputs = tokenizer.encode(extracted_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=512, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        st.text_area(f"Summary of {file.name}:", summary, height=300)
