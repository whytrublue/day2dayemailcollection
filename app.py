import pandas as pd
import streamlit as st
import re
import io

# Function to process the pasted data
def process_email_data(pasted_data):
    # Split using any sequence of 10+ of -, =, _, or +
    data_blocks = re.split(r'[-=_+]{10,}', pasted_data)

    processed_data = [["First Name", "Last Name", "Email"]]

    for block in data_blocks:
        lines = block.strip().split("\n")
        for line in lines:
            line = line.strip()
            line = re.sub(r'\s+', ' ', line)  # normalize spaces
            email_match = re.search(r'\S+@\S+', line)
            if email_match:
                email = email_match.group(0).strip()
                name = line.replace(email, '').strip()
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

# Bigger example line
st.markdown("""
### 📌 Example:
<div style='font-size:18px; font-weight:bold;'>babu reddy babu@gmail.com</div>
""", unsafe_allow_html=True)

# Text area for pasting
pasted_data = st.text_area("Paste your text data here", height=300)

# Extract button
if st.button("Extract Data"):
    if pasted_data.strip():
        processed_data = process_email_data(pasted_data)
        df = pd.DataFrame(processed_data[1:], columns=processed_data[0])

        st.subheader("Copy to Clipboard (Paste into Excel or Sheets)")
        tsv_text = df.to_csv(index=False, sep='\t')
        st.code(tsv_text, language='text')

        output_file = io.BytesIO()
        df.to_csv(output_file, index=False)
        output_file.seek(0)
        st.download_button("Download Processed CSV", output_file, file_name="Names_Separated.csv", mime="text/csv")
    else:
        st.warning("Please paste some data to extract.")

# Clear button
if st.button("Clear Data"):
    st.experimental_rerun()
