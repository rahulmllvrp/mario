import streamlit as st
from PIL import Image
import os

# Create a title for the app
st.title("Employee Year-End Reports")

# Left sidebar with employee names and larger images
st.sidebar.title("Employees")

# Updated list of employee names and their respective images
employees = {
    "Aish": "images/aish_image.png",
    "Rahul": "images/rahul_image.png",
    "Eldridge": "images/eldridge_image.png",
    "Jackson": "images/jackson_image.png"
}

# Variable to hold the name of the selected employee
selected_employee = None

# Function to display the image and name side by side, with centered name
def display_employee(name, image_path):
    global selected_employee
    if os.path.exists(image_path):
        # Create two equal columns: one for the image, one for the name
        cols = st.sidebar.columns([1, 1])  # Adjust the width ratio if needed
        with cols[0]:  # First column for the image
            st.image(image_path, width=110)  # Set the image width here
        
        # Add some vertical space before the name button
        with cols[1]:  # Second column for the name (center-aligned vertically)
            st.markdown("<br>", unsafe_allow_html=True)  # Add space
            st.button(name, key=name)  # Name acts as a clickable button
            if st.session_state.get(name) == True:  # Check if the button was clicked
                selected_employee = name  # Store the selected employee's name
        
        # Add a horizontal line to separate employees
        st.sidebar.markdown("<hr style='border: 1px solid dark gray;'>", unsafe_allow_html=True)

# Function to display the report for the selected employee
def show_report(employee_name):
    st.markdown(
        f"<div style='text-align: center;'><h2>Year-End Report for {employee_name}</h2></div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='text-align: center;'>This is the detailed report for {employee_name}.</div>",
        unsafe_allow_html=True
    )

# Display each employee in the sidebar
for name, image_path in employees.items():
    display_employee(name, image_path)

# Center report in the main section when an employee is selected
if selected_employee:
    show_report(selected_employee)

# Bottom section with a search or analysis feature
st.subheader("Analysis")
search_query = st.text_input("Ask me anything")  # Replacing 'search report' with 'Ask me anything'

# Simulate an analysis result for the user's query
if search_query:
    st.write(f"Analysis for '{search_query}'")  # You can integrate AI analysis here
    st.write("This would show a detailed analysis based on the employee's data and the search query.")
