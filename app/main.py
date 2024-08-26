import streamlit as st
import os
import json
import uuid
from dotenv import load_dotenv
from app.file_processor import process_file
from app.data_extractor import extract_sections, retrieve_sections
from app.user_prompts import prompt_for_missing_info
from app.startup_metrics import calculate_metrics
from app.report_generator import generate_report
from app.config import IBM_API_KEY, IBM_CLOUD_URL, PROJECT_ID
import requests
from sqlalchemy import create_engine, text
from datetime import datetime

load_dotenv()

UPLOADS_DIR = "uploads"
METADATA_FILE = "uploads_metadata.json"

# Ensure the uploads directory exists
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Database connection
db_url = os.getenv("SINGLESTORE_URL")
print(f"Database URL: {db_url}")  # Debug print to check the database URL
singlestore_url = f"singlestoredb://{db_url}"
engine = create_engine(singlestore_url)

def create_pitchdeck_upload_table():
    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS pitchdeck_upload (
                id SERIAL PRIMARY KEY,
                startup_id VARCHAR(255),
                file_path TEXT,
                original_filename TEXT,
                user_email TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """))

def insert_pitchdeck_upload(startup_id, file_path, original_filename, user_email):
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            INSERT INTO pitchdeck_upload (startup_id, file_path, original_filename, user_email, created_at, updated_at)
            VALUES (:startup_id, :file_path, :original_filename, :user_email, :created_at, :updated_at)
            RETURNING id
        """), {
            "startup_id": startup_id,
            "file_path": file_path,
            "original_filename": original_filename,
            "user_email": user_email,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        file_id = result.fetchone()[0]
    return file_id

def save_metadata(file_id, file_path, original_filename, user_email):
    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)
    metadata[file_id] = {
        "file_path": file_path,
        "original_filename": original_filename,
        "user_email": user_email
    }
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)

def main():
    st.title("VC Pitch Simulator")
    st.write("Upload your startup pitch deck and get professional VC analysis.")

    # Get user's email
    user_email = st.text_input("Enter your email")

    # Display process diagram
    st.subheader("Process Overview")
    st.markdown("""
    1. **Upload your pitch deck file**
    2. **File is processed and broken down into sections: Team, Fundraising, Market, Product, Business Model, Traction, and Other**
    3. **Check the level of completion of information and prompt for missing info if necessary**
    4. **Send updated info for feedback and analysis by the LLM using the Knowledge Base**
    5. **Prompt user to start a 'VC Session' for detailed analysis and action plan for qualifying for a certain round**
    """)

    uploaded_file = st.file_uploader("Choose your pitch deck file", type=["pdf", "docx", "txt"], key="file_uploader")

    if uploaded_file is not None and user_email:
        # Generate a unique ID for the uploaded file
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(uploaded_file.name)[1]
        original_filename = os.path.splitext(uploaded_file.name)[0]
        uploaded_file_path = os.path.join(UPLOADS_DIR, f"{file_id}{file_extension}")

        # Save the uploaded file temporarily with its original extension
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Save metadata
        save_metadata(file_id, uploaded_file_path, original_filename, user_email)

        # Create the pitchdeck_upload table if it doesn't exist
        create_pitchdeck_upload_table()

        # Insert data into the pitchdeck_upload table and get the file_id
        file_id = insert_pitchdeck_upload(file_id, uploaded_file_path, original_filename, user_email)

        with st.spinner("Processing your pitch deck for completion..."):
            # Process the file and extract text
            extracted_content, content_id = process_file(uploaded_file_path, file_id, original_filename, user_email)

            # Process the pitch deck and store section data
            extract_sections(uploaded_file_path, file_id, content_id)

        # Fetch the extracted data from the database
        extracted_data = retrieve_sections(startup_id=file_id)

        # Display extracted data in two columns
        st.subheader("Extracted Startup Data")
        col1, col2 = st.columns(2)
        sections = list(extracted_data.keys())
        for i, section in enumerate(sections):
            with col1 if i % 2 == 0 else col2:
                st.write(f"### {section.capitalize()}")
                st.json(extracted_data[section])

        # Prompt user to confirm or provide more information
        st.subheader("Additional Information")
        for section in sections:
            with st.expander(f"Provide more information for {section.capitalize()}"):
                additional_info = st.text_area(f"Additional information for {section.capitalize()}")
                if additional_info:
                    # Update the extracted data with additional information
                    extracted_data[section] += "\n" + additional_info

        # Check completeness and prompt for missing information if necessary
        if not extracted_data or len(extracted_data) < 5:  # Adjust the condition based on your completeness criteria
            st.warning("We couldn't find enough information. Our chat assistant wants to ask a few questions.")
            complete_startup_data = prompt_for_missing_info(extracted_data)
        else:
            complete_startup_data = extracted_data

        # Calculate startup metrics
        metrics = calculate_metrics(complete_startup_data)

        # Generate and display report
        report = generate_report(complete_startup_data, metrics)
        st.subheader("VC Analysis Report")
        st.write(report)

        # Prompt user for VC Session
        if st.button("Start VC Session"):
            st.write("Starting VC Session...")
            # Add logic for VC Session here

if __name__ == "__main__":
    main()
