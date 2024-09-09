FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    apt-utils \
    build-essential \
    curl \
    software-properties-common \
    bash \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /app/venv

COPY . /app
RUN source /app/venv/bin/activate


RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "run.py", "--server.port=8501", "--server.headless=True", "--server.enableCORS=False", "--server.enableXsrfProtection=False"]
