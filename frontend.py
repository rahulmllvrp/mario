import os
import PyPDF2
import google.generativeai as genai
import streamlit as st

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

# Streamlit Interface
st.title("Employee Year-End Report Analysis")

# Sidebar for employee selection
st.sidebar.title("Select an Employee")

# Employees dictionary (name and image)
employees = {
    "Aish": "images/aish_image.png",
    "Rahul": "images/rahul_image.png",
    "Eldridge": "images/eldridge_image.png",
    "Jackson": "images/jackson_image.png"
}

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
                analysis_result = analyze_query(report_text, query)
                if analysis_result:
                    st.write(f"Response: {analysis_result}")
    else:
        st.error(f"No report found for {selected_employee}.")
