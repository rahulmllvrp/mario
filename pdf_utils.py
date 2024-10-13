import base64
import PyPDF2
import streamlit as st

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_number in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_number].extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading {pdf_path}: {e}")
        return ""

# Function to display PDFs in Streamlit app
def display_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding the PDF using HTML iframe
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    return pdf_display
