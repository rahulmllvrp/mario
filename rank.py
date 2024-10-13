import os
import google.generativeai as genai
import PyPDF2
## from docx import Document

# Set up API key for Gemini
os.environ["API_KEY"] = "AIzaSyCiElgnWd-dN78SKIit8h6E0gj9hl7U6GQ"
genai.configure(api_key=os.environ["API_KEY"])

# Configurations for AI output - variables
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1
}

model = genai.GenerativeModel("gemini-pro")

# Define path to PDF year-end reports
path = "Data/YER"

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
        print(f"Error reading {pdf_path}: {e}")
        return ""

# Function to analyze text using Gemini AI
def analyze_report(report_text):
    input_text = f"Analyze the following year-end report and provide a score from 1 to 10 (i just want the number and nothing else... i.e 9) based on the individual's contribution to the company:\n\n{report_text}"
    
    response = model.generate_content(input_text)
    score_text = response.text.strip()
    # Extract score from the response (assumes Gemini will provide a clear score)
    try:
        score = int(score_text.split()[-1])  # Simplistic score extraction
        print(score)
        return score
    except:
        return None

# Process all PDF reports and analyze
scores = {}
for file_name in os.listdir(path):
    if file_name.endswith(".pdf"):
        # Extract text from PDF
        pdf_path = os.path.join(path, file_name)
        report_text = extract_text_from_pdf(pdf_path)
        
        if report_text:
            # Analyze the report
            score = analyze_report(report_text)
            
            if score is not None:
                scores[file_name] = score
                print(f"{file_name} - Score: {score}")
            else:
                print(f"Could not extract a valid score for {file_name}")
        else:
            print(f"No text extracted from {file_name}")

# Rank the individuals based on their scores
ranked_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

for rank, (file_name, score) in enumerate(ranked_scores, 1):
    print(f"{rank}. {file_name} - Score: {score}/10")

# Output ranking to a Word document
# doc = Document()
# doc.add_heading("Year-End Report Ranking", 0)

# for rank, (file_name, score) in enumerate(ranked_scores, 1):
#     doc.add_paragraph(f"{rank}. {file_name} - Score: {score}/10")

# doc_path = os.path.join(output_folder, "Year-End_Report_Rankings.docx")
# doc.save(doc_path)

# print(f"\nAnalysis complete. Ranking saved to: {doc_path}")
