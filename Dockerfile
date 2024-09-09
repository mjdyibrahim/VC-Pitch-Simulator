FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    pip3 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /app/venv

COPY . /app
RUN . /app/venv/bin/activate

# Set environment variable to use system-wide Python packages
ENV PYTHONPATH=/usr/local/lib/python3.11/dist-packages:$PYTHONPATH

# RUN /app/venv/bin/pip install --upgrade pip
# RUN /app/venv/bin/pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "run.py", "--server.port=8501", "--server.headless=True", "--server.enableCORS=False", "--server.enableXsrfProtection=False"]
