# EHCP Report Generator

This is a simple Streamlit app that generates summaries from EHCP documents (PDF or DOCX) using a pre-trained BART model.

## Features
- Upload multiple EHCP documents
- Extracts text from PDFs and Word documents
- Summarises content using HuggingFace Transformers

## Setup

```bash
pip install -r requirements.txt
streamlit run ehcp_free_generator.py
```

## Deployment
You can deploy this on Hugging Face Spaces or Streamlit Cloud.