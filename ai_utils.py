import PyPDF2
import google.generativeai as genai
import os
import streamlit as st

# Set up API key for Gemini
os.environ["API_KEY"] = "AIzaSyCiElgnWd-dN78SKIit8h6E0gj9hl7U6GQ"
genai.configure(api_key=os.environ["API_KEY"])

# Function to analyze a report based on a user's query
def analyze_query(report_text, query):
    input_text = f"Based on the following year-end report, {query}\n\n{report_text}"
    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(input_text)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error analyzing the query: {e}")
        return None
    
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

# Function to analyze employee report text
def analyze_report(report_text):
    input_text = f"Please analyze the following year-end reports and provide a score from 1 to 10 for each individual based on their contribution to the company, without repeating the word 'score' or adding '/10' more than once. Additionally, evaluate whether the individual should act as a mentor or a mentee within the group and suggest who they should mentor or be mentored by. Please analyze the following year-end reports and provide a score from 1 to 10 for each individual based on their contribution to the company, without repeating the word 'score' or adding '/10' more than once. Additionally, evaluate whether the individual should act as a mentor or a mentee within the group and suggest who they should mentor or be mentored by. The score should be presented only once, in the format Score: X/10 with no additional formatting or repetition, followed by the mentorship recommendation and rationale.:\n\n{report_text}"
    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(input_text)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error analyzing the report: {e}")
        return None

# Function to analyze project descriptions against selected employees
def analyze_project_against_employees(project_description, selected_employees, reports_path):
    selected_employee_reports = ""

    # Loop over the selected employees and extract their reports
    for employee in selected_employees:
        pdf_file_path = os.path.join(reports_path, f"{employee}_YER.pdf")
        employee_report_text = extract_text_from_pdf(pdf_file_path)

        if employee_report_text:
            selected_employee_reports += f"\nReport for {employee}:\n{employee_report_text}\n"

    # If we have valid reports, analyze them using AI
    if selected_employee_reports:
        input_text = (
            f"Based on the following project description and year-end reports of the selected employees, analyze which individual is best suited to take on the project. "
            f"Additionally, suggest who among them should be the team leader based on their strengths, leadership skills, and ability to manage the team effectively.\n\n"
            f"Project Description:\n{project_description}\n\nSelected Employee Reports:\n{selected_employee_reports}"
        )

        try:
            job_analysis_result = genai.GenerativeModel("gemini-pro").generate_content(input_text).text.strip()
            return job_analysis_result
        except Exception as e:
            return f"Error analyzing the project: {e}"

    else:
        return "No valid reports found for the selected employees."