import streamlit as st
import os
from dotenv import load_dotenv
from app.file_processor import process_file
from app.data_extractor import extract_data
from app.user_prompts import prompt_for_missing_info
from app.startup_metrics import calculate_metrics
from app.report_generator import generate_report
from app.config import IBM_API_KEY, IBM_CLOUD_URL, PROJECT_ID
import requests

load_dotenv()

def main():
    st.title("Venture Capital Assistant")
    st.write("Upload your startup pitch deck and get professional VC analysis.")

    uploaded_file = st.file_uploader("Choose your pitch deck file", type=["pdf", "docx", "txt"], key="file_uploader")

    if uploaded_file is not None:
        # Save the uploaded file temporarily with its original extension
        temp_file_path = f"temp_pitch_deck{os.path.splitext(uploaded_file.name)[1]}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the file and extract text
        text_content = process_file(temp_file_path)

        # Extract data using IBM Granite Model
        schema_path = "data/startup_profile_schema.json"
        prompts_path = "data/startup_profile_prompts.json"
        startup_data = extract_data(text_content, schema_path, prompts_path)

        # Display extracted data
        st.subheader("Extracted Startup Data")
        st.json(startup_data)

        # Prompt user for missing information
        st.subheader("Additional Information")
        complete_startup_data = prompt_for_missing_info(startup_data)

        # Calculate startup metrics
        metrics = calculate_metrics(complete_startup_data)

        # Generate and display report
        report = generate_report(complete_startup_data, metrics)
        st.subheader("VC Analysis Report")
        st.write(report)

        # Clean up temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()