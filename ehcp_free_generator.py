import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration
from docx import Document
import pdfplumber

# Streamlit setup
st.set_page_config(page_title="EHCP Generator", layout="wide")
st.title("📄 EHCP Report Generator")

# Load model
@st.cache_resource
def load_model():
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
    return model, tokenizer

model, tokenizer = load_model()

# --- Input Fields ---
student_name = st.text_input("Student Name")
year_group = st.text_input("Year Group")
additional_info = st.text_area("Additional Information (Optional)")

# --- Multi-File Upload ---
uploaded_files = st.file_uploader("Upload Supporting Documents (.pdf or .docx)", type=["pdf", "docx"], accept_multiple_files=True)
extracted_texts = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = uploaded_file.name.split(".")[-1].lower()

        if file_ext == "docx":
            doc = Document(uploaded_file)
            file_text = "\n".join([para.text for para in doc.paragraphs])

        elif file_ext == "pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                file_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

        extracted_texts.append(f"--- Extracted from: {uploaded_file.name} ---\n{file_text}")

    combined_text = "\n\n".join(extracted_texts)

    st.subheader("🧾 Combined Extracted Text")
    
