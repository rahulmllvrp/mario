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
def analyze_report(report_text):
    input_text = f"Please analyze the following year-end reports and provide a score from 1 to 10 for each individual based on their contribution to the company, without repeating the word 'score' or adding '/10' more than once. Additionally, evaluate whether the individual should act as a mentor or a mentee within the group and suggest who they should mentor or be mentored by. Please analyze the following year-end reports and provide a score from 1 to 10 for each individual based on their contribution to the company, without repeating the word 'score' or adding '/10' more than once. Additionally, evaluate whether the individual should act as a mentor or a mentee within the group and suggest who they should mentor or be mentored by. The score should be presented only once, in the format Score: X/10 with no additional formatting or repetition, followed by the mentorship recommendation and rationale.:\n\n{report_text}"
    
    try:
        response = model.generate_content(input_text)
        score_text = response.text.strip()
        return score_text
    except Exception as e:
        st.error(f"Error analyzing the report: {e}")
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
        pdf_file_path = os.path.join(path, f"{selected_employee}_year_end_report.pdf")

        if os.path.exists(pdf_file_path):
            # Extract and display the text from the PDF
            report_text = extract_text_from_pdf(pdf_file_path)
            
            if report_text:
                st.text_area("Extracted Report Text", report_text, height=300)

                # Chatbot feature: User can ask questions
                query = st.text_input("Ask a question about the report")
                if query:
                    # Analyze based on the user's query
                    analysis_result = analyze_report(report_text)
                    if analysis_result:
                        st.write(f"Response: {analysis_result}")
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
            file_name = f"{employee}_year_end_report.pdf"  # Get the respective PDF file name
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
    if st.button("Action 1"):
        if selected_employees:
            # Rank the selected employees
            ranked_scores = rank_selected_employees(selected_employees)
            
            st.write("### Ranking of Selected Employees")
            for rank, (employee, score) in enumerate(ranked_scores, 1):
                st.write(f"{rank}. {employee} - {score}")
        else:
            st.warning("No employees selected.")

    # Placeholder for Action 2
    if st.button("Action 2"):
        st.write("Action 2 triggered.")
