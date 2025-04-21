import pandas as pd
import streamlit as st
import re
import io

# Function to process the pasted data
def process_email_data(pasted_data):
    # Split the content into blocks separated by "-------------" or "============="
    data_blocks = re.split(r'[-=]{10,}', pasted_data)

    # Initialize the processed data
    processed_data = [["First Name", "Last Name", "Email"]]  # Header row

    # Process each block of data
    for block in data_blocks:
        lines = block.strip().split("\n")
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
                    first_name = name_parts[0].capitalize()
                    last_name = " ".join([part.capitalize() for part in name_parts[1:]])
                else:
                    first_name = name_parts[0].capitalize()
                    last_name = ""
                processed_data.append([first_name, last_name, email])

    return processed_data

# Streamlit UI
st.title("Email and Name Processor")

# Text area for pasting the dataset
pasted_data = st.text_area("Paste your text data here", height=300)

# Buttons to process and clear data
if st.button("Extract Data"):
    if pasted_data.strip():
        # Process the pasted data
        processed_data = process_email_data(pasted_data)

        # Display the data in a table
        st.subheader("Processed Data")
        df = pd.DataFrame(processed_data[1:], columns=processed_data[0])
        st.dataframe(df)

        # Show TSV content for easy Excel copy-paste
        st.subheader("Copy to Clipboard (Paste into Excel or Sheets)")
        tsv_text = df.to_csv(index=False, sep='\t')
        st.code(tsv_text, language='text')

        # Convert to CSV for download
        output_file = io.BytesIO()
        df.to_csv(output_file, index=False)
        output_file.seek(0)

        # Provide download link for the CSV file
        st.download_button("Download Processed CSV", output_file, file_name="Names_Separated.csv", mime="text/csv")
    else:
        st.warning("Please paste some data to extract.")

# Clear the pasted data
if st.button("Clear Data"):
    st.experimental_rerun()
