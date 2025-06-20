import gradio as gr
import pdfplumber
import docx
from transformers import BartForConditionalGeneration, BartTokenizer

# Load model and tokenizer
model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")

# Function to extract text
def extract_text(files):
    all_text = ""
    for file in files:
        if file.name.endswith(".pdf"):
            with pdfplumber.open(file.name) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"
        elif file.name.endswith(".docx"):
            doc = docx.Document(file.name)
            for para in doc.paragraphs:
                all_text += para.text + "\n"
    return all_text

# Function to summarize
def summarize(files):
    raw_text = extract_text(files)
    inputs = tokenizer.encode(raw_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=200, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Gradio Interface
interface = gr.Interface(
    fn=summarize,
    inputs=gr.File(file_types=[".pdf", ".docx"], file_count="multiple"),
    outputs="text",
    title="EHCP Report Generator",
    description="Upload multiple PDF or Word EHCP documents to generate a summary."
)

interface.launch()
