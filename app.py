import pandas as pd
import streamlit as st
import csv
import re
import io

# Function to process the data from the uploaded file
def process_email_file(uploaded_file):
    # Read the file
    lines = uploaded_file.getvalue().decode("utf-8").splitlines()

    # Process the data
    processed_data = [["First Name", "Last Name", "Email"]]  # Header row
    for line in lines:
        # Use regular expression to extract the email
        email_match = re.search(r'\S+@\S+', line)  # Match email format
        if email_match:
            email = email_match.group(0)  # Extract email
            # Remove email from line to isolate the name
            name = line.replace(email, '').strip()
            # Separate the name into parts
            name_parts = name.split()
            if len(name_parts) > 1:
                first_name = name_parts[0]
                last_name = " ".join(name_parts[1:])  # Join the rest as last name
            else:
                first_name = name_parts[0]
                last_name = ""  # No last name found
            processed_data.append([first_name, last_name, email])

    # Convert the processed data to CSV in memory
    output_file = io.BytesIO()
    writer = csv.writer(output_file)
    writer.writerows(processed_data)
    output_file.seek(0)  # Rewind the buffer to the beginning

    return output_file

# Streamlit UI
st.title(" Full Name and Email Address followed by dashlines ------")

# File uploader for the user to upload the file
uploaded_file = st.file_uploader("Upload your text file", type=["txt"])

if uploaded_file is not None:
    # Process the uploaded file
    output_file = process_email_file(uploaded_file)

    # Provide download button for the CSV file
    st.download_button("Download Processed CSV", output_file, file_name="Names_Separated.csv", mime="text/csv")
