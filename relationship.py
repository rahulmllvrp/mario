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
path = r"./Data/YER"

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
def analyze_report(report_text, prompt):
    input_text = f"{prompt}:\n\n{report_text}"
    response = model.generate_content(input_text)
    return response.text.strip()

# Process all PDF reports and analyze
reports = {}
for file_name in os.listdir(path):
    if file_name.endswith(".pdf"):
        # Extract text from PDF
        pdf_path = os.path.join(path, file_name)
        report_text = extract_text_from_pdf(pdf_path)
        
        if report_text:
            # Analyze the report
            report = analyze_report(report_text, "Analyze the following year-end report and take note of their strengths and weaknesses beacuse you're going to compare this person's strengths and weaknesses to the next and decide who they should work with so that the company can propel forwards... bascially form mentee/mentor relationships. write the the form of [name: stength/weakness]")
            
            if report is not None:
                reports[file_name] = report
                #print(f"{file_name} - report: {report}")
            else:
                print(f"Could not extract a valid report for {file_name}")
        else:
            print(f"No text extracted from {file_name}")

final_reports = reports.items()
answer = analyze_report(final_reports, "Out of the following individuals what mentor mentee pairs can we make in order for there to be an effective flow of knwoledge and boost production. There can be a mentor to more than one mentee. Give me your asnwer in this format <Mentor Name>: <Mentee(s) Names> for <the reasons why the relatiosnhip has formed>")
print(answer)

# Output ranking to a Word document
# doc = Document()
# doc.add_heading("Year-End Report Ranking", 0)

# for rank, (file_name, score) in enumerate(ranked_scores, 1):
#     doc.add_paragraph(f"{rank}. {file_name} - Score: {score}/10")

# doc_path = os.path.join(output_folder, "Year-End_Report_Rankings.docx")
# doc.save(doc_path)

# print(f"\nAnalysis complete. Ranking saved to: {doc_path}")
