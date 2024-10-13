import streamlit as st
import os
from pdf_utils import extract_text_from_pdf, display_pdf
from ai_utils import analyze_query, analyze_report, analyze_project_against_employees 

# Define path to PDF year-end reports and project descriptions
path = "Data/YER"
project_descriptions_path = "Data/PD"

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
    if st.sidebar.button("Employee Compatibility Test"):
        st.session_state.screen = "compatibility_test"
        st.rerun()

elif st.session_state.screen == "compatibility_test":
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

        pdf_file_path = os.path.join(path, f"{selected_employee}_YER.pdf")

        if os.path.exists(pdf_file_path):
            # Embed and display the PDF in the app
            st.markdown(display_pdf(pdf_file_path), unsafe_allow_html=True)

            # Custom label for input box
            st.markdown("<p class='big-font'>Ask a question about the report</p>", unsafe_allow_html=True)
            query = st.text_area("", placeholder="Type your question here...", height=150)

            if query:
                report_text = extract_text_from_pdf(pdf_file_path)  # Extract text from PDF for analysis
                analysis_result = analyze_query(report_text, query)
                if analysis_result:
                    st.write(f"{analysis_result}")
        else:
            st.error(f"No report found for {selected_employee}.")

# Compatibility Test Screen
if st.session_state.screen == "compatibility_test":
    st.title("Employee Compatibility Test")

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
            file_name = f"{employee}_YER.pdf"
            pdf_path = os.path.join(path, file_name)
            report_text = extract_text_from_pdf(pdf_path)

            if report_text:
                score = analyze_report(report_text)
                if score is not None:
                    scores[employee] = score
                else:
                    st.error(f"Could not extract a valid score for {employee}")
            else:
                st.error(f"No text extracted from {employee}'s report")

        ranked_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_scores

    if st.button("Ranking and Mentorship"):
        if selected_employees:
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
                project_analysis_result = analyze_project_against_employees(project_description, selected_employees, path)
                if project_analysis_result:
                    st.write(f"### {project_name} Analysis Results")
                    st.write(project_analysis_result)
            else:
                st.error(f"Could not extract text from {project_file}.")
