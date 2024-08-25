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

def call_ibm_granite(text):
    headers = {
        "Authorization": f"Bearer {IBM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model_id": "granite-13b-chat-v2",
        "inputs": [text],
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 0,
            "stop_sequences": [],
            "repetition_penalty": 1
        },
        "project_id": PROJECT_ID
    }
    
    response = requests.post(f"{IBM_CLOUD_URL}/ml/v1-beta/generation/text", headers=headers, json=data)
    return response.json()

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
        startup_data = extract_data(text_content)

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
        os.remove("temp_pitch_deck")

if __name__ == "__main__":
    main()
