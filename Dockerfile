FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    apt-utils \
    git \
    pip \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /app/venv

COPY . /app
RUN . /app/venv/bin/activate


RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["/app/venv/bin/streamlit", "run", "run.py", "--server.port=8501", "--server.headless=True", "--server.enableCORS=False", "--server.enableXsrfProtection=False"]
