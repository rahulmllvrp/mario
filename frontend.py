import base64
from io import BytesIO
import os
import PyPDF2
import google.generativeai as genai
import streamlit as st

# Set up API key for Gemini
os.environ["API_KEY"] = "AIzaSyCiElgnWd-dN78SKIit8h6E0gj9hl7U6GQ"  # Replace with your actual API key
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
project_descriptions_path = "Data/PD"

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

# Function to analyze text using Gemini AI
def analyze_query(report_text, query):
    input_text = f"Based on the following year-end report, {query}\n\n{report_text}"
    
    try:
        response = model.generate_content(input_text)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error analyzing the query: {e}")
        return None
    
def display_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Embedding the PDF using HTML iframe
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    
    return pdf_display


# Function to analyze text using Gemini AI
def analyze_report(report_text):
    input_text = f"Please analyze the following year-end reports and provide a score from 1 to 10 for each individual based on their contribution to the company, without repeating the word 'score' or adding '/10' more than once. Additionally, evaluate whether the individual should act as a mentor or a mentee within the group and suggest who they should mentor or be mentored by. Please analyze the following year-end reports and provide a score from 1 to 10 for each individual based on their contribution to the company, without repeating the word 'score' or adding '/10' more than once. Additionally, evaluate whether the individual should act as a mentor or a mentee within the group and suggest who they should mentor or be mentored by. The score should be presented only once, in the format Score: X/10 with no additional formatting or repetition, followed by the mentorship recommendation and rationale.:\n\n{report_text}"
    
    try:
        response = model.generate_content(input_text)
        score_text = response.text.strip()
        return score_text
    except Exception as e:
        st.error(f"Error analyzing the report: {e}")
        return None
    
# Function to analyze project description against selected employees' reports
def analyze_project_against_employees(project_description, selected_employees):
    selected_employee_reports = ""
    for employee in selected_employees:
        pdf_file_path = os.path.join(path, f"{employee}_YER.pdf")
        selected_employee_report_text = extract_text_from_pdf(pdf_file_path)
        if selected_employee_report_text:
            selected_employee_reports += f"\nReport for {employee}:\n{selected_employee_report_text}\n"

    if selected_employee_reports:
        # Create input for Gemini based on project description and employee reports
        input_text = f"Based on the following project description and year-end reports of the selected employees, analyze which individual is best suited to take on the project. Additionally, suggest who among them should be the team leader based on their strengths, leadership skills, and ability to manage the team effectively.\n\nProject Description:\n{project_description}\n\nSelected Employee Reports:\n{selected_employee_reports}"
        
        job_analysis_result = model.generate_content(input_text).text.strip()
        return job_analysis_result
    else:
        st.warning("No valid reports found for the selected employees.")
        return None


# Sidebar menu heading styled to appear next to the arrow
st.sidebar.markdown("Menu")

# Employees dictionary (name and image)
employees = {
    "Aish": "images/aish_image.png",
    "Rahul": "images/rahul_image.png",
    "Eldridge": "images/eldridge_image.png",
    "Jackson": "images/jackson_image.png"
}

# Session state to switch between views
if "screen" not in st.session_state:
    st.session_state.screen = "year_end_report"  # Default screen shows year-end report analysis

# Toggle button logic based on the current screen
if st.session_state.screen == "year_end_report":
    # Show button to switch to compatibility test
    if st.sidebar.button("Employee Compatibility Test"):
        st.session_state.screen = "compatibility_test"
        st.rerun()

elif st.session_state.screen == "compatibility_test":
    # Show button to switch to year-end report analysis
    if st.sidebar.button("Employee Year-End Report Analysis"):
        st.session_state.screen = "year_end_report"
        st.rerun()

# Year-End Report Screen
if st.session_state.screen == "year_end_report":
    st.title("Employee Year-End Report Analysis")

    # Display employee images and buttons in the sidebar
    selected_employee = st.sidebar.selectbox("Choose an Employee", list(employees.keys()))

    # Display the employee image if it exists
    if selected_employee:
        image_path = employees[selected_employee]
        if os.path.exists(image_path):
            st.sidebar.image(image_path, caption=selected_employee, use_column_width=True)
        else:
            st.sidebar.error(f"Image not found for {selected_employee}.")

    # Main Section
    if selected_employee:
        st.subheader(f"Year-End Report for {selected_employee}")

        # Construct the file name based on the selected employee
        pdf_file_path = os.path.join(path, f"{selected_employee}_YER.pdf")

        if os.path.exists(pdf_file_path):
            # Embed and display the PDF in the app
            st.markdown(display_pdf(pdf_file_path), unsafe_allow_html=True)

            # Custom CSS to increase the font size of the label text
            st.markdown(
                """
                <style>
                .big-font {
                    font-size: 24px !important;
                    font-weight: bold;
                    margin-bottom: -200px; 
                }
                </style>
                <p class="big-font">Ask a question about the report</p>
                """, 
                unsafe_allow_html=True
            )

            # Chatbot feature: User can ask questions (input box remains the same size)
            query = st.text_area("", placeholder="Type your question here...", height=150)

            if query:
                # Analyze based on the user's query
                report_text = extract_text_from_pdf(pdf_file_path)  # Extract text from PDF for analysis
                analysis_result = analyze_query(report_text, query)
                if analysis_result:
                    st.write(f"{analysis_result}")
        else:
            st.error(f"No report found for {selected_employee}.")


# Compatibility Test Screen
if st.session_state.screen == "compatibility_test":
    st.title("Employee Compatibility Test")

    # Multi-select for employees (no "ALL" option)
    selected_employees = st.multiselect("Select employees for compatibility analysis", list(employees.keys()))

    # Sidebar for displaying selected employee images
    if selected_employees:
        st.sidebar.markdown("### Selected Employees")
        for employee in selected_employees:
            image_path = employees[employee]
            if os.path.exists(image_path):
                st.sidebar.image(image_path, caption=employee, use_column_width=True)
            else:
                st.sidebar.error(f"Image not found for {employee}.")

    # Function to rank selected employees based on their report scores
    def rank_selected_employees(selected_employees):
        scores = {}
        
        for employee in selected_employees:
            file_name = f"{employee}_YER.pdf"  # Get the respective PDF file name
            pdf_path = os.path.join(path, file_name)
            
            # Extract text from PDF
            report_text = extract_text_from_pdf(pdf_path)
            
            if report_text:
                # Analyze the report using AI
                score = analyze_report(report_text)
                if score is not None:
                    scores[employee] = score
                else:
                    st.error(f"Could not extract a valid score for {employee}")
            else:
                st.error(f"No text extracted from {employee}'s report")

        # Rank the individuals based on their scores
        ranked_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return ranked_scores

    # Action 1: Analyze and Rank selected employees
    if st.button("Ranking and Mentorship"):
        if selected_employees:
            # Rank the selected employees
            ranked_scores = rank_selected_employees(selected_employees)
            
            st.write("### Ranking of Selected Employees")
            for rank, (employee, score) in enumerate(ranked_scores, 1):
                st.write(f"{rank}. {employee} - {score}")
        else:
            st.warning("No employees selected.")

    # Add a line separator between Action 1 and the projects
    st.write("---")

    # Project Buttons
    st.write("### Choose a Project")
    project_files = [
        ("AI-Powered Year-End Report Analyzer Project", "PD_1.pdf"),
        ("AI-Driven Port Resilience Monitoring System", "PD_2.pdf"),
        ("Sustainable Supply Chain Carbon Tracker", "PD_3.pdf"),
        ("AI-Powered Workforce Engagement and Well-Being Platform", "PD_4.pdf"),
        ("Digital Twin for Port Operations Optimization", "PD_5.pdf"),
        ("Intermodal Logistics AI Optimizer", "PD_6.pdf")
    ]

    for project_name, project_file in project_files:
        if st.button(project_name):
            # Extract text from the selected project PDF
            project_pdf_path = os.path.join(project_descriptions_path, project_file)
            project_description = extract_text_from_pdf(project_pdf_path)

            if project_description:
                # Analyze the project against the selected employees
                project_analysis_result = analyze_project_against_employees(project_description, selected_employees)
                if project_analysis_result:
                    st.write(f"### {project_name} Analysis Results")
                    st.write(project_analysis_result)
            else:
                st.error(f"Could not extract text from {project_file}.")