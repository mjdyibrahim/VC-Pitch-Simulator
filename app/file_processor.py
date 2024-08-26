import fitz  # PyMuPDF
import docx
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Database connection
db_url = os.getenv("SINGLESTORE_URL")
singlestore_url = f"singlestoredb://{db_url}"
engine = create_engine(singlestore_url)

def create_pitchdeck_content_table():
    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS pitchdeck_content (
                id SERIAL PRIMARY KEY,
                startup_id VARCHAR(255),
                file_id VARCHAR(255),
                file_path TEXT,
                original_filename TEXT,
                user_email TEXT,
                extracted_content TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                FOREIGN KEY (file_id) REFERENCES pitchdeck_upload(id)
            )
        """))

def insert_pitchdeck_content(startup_id, file_id, file_path, original_filename, user_email, extracted_content):
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            INSERT INTO pitchdeck_content (startup_id, file_id, file_path, original_filename, user_email, extracted_content, created_at, updated_at)
            VALUES (:startup_id, :file_id, :file_path, :original_filename, :user_email, :extracted_content, :created_at, :updated_at)
            RETURNING id
        """), {
            "startup_id": startup_id,
            "file_id": file_id,
            "file_path": file_path,
            "original_filename": original_filename,
            "user_email": user_email,
            "extracted_content": extracted_content,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        content_id = result.fetchone()[0]
    return content_id

def process_file(file_path, startup_id, file_id, original_filename, user_email):
    file_extension = os.path.splitext(file_path)[1].lower()
    print(f"Processing file: {file_path}, File extension: {file_extension}")  # Debug statement
    
    if file_extension == '.pdf':
        extracted_content = extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        extracted_content = extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        extracted_content = extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file type")

    # Create the pitchdeck_content table if it doesn't exist
    create_pitchdeck_content_table()

    # Insert data into the pitchdeck_content table and get the content_id
    content_id = insert_pitchdeck_content(startup_id, file_id, file_path, original_filename, user_email, extracted_content)

    return extracted_content, content_id

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text