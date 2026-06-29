FROM python:3.9-slim

WORKDIR /app

# Install system compilation dependencies required for building FAISS & general packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Prefetch the sentence transformer weights so it doesn't download at runtime inside Docker
RUN python -c "from sentence_transformers import SentenceTransformer; Model = SentenceTransformer('all-MiniLM-L6-v2')"

COPY . .

# Run preprocess automatically to set up vector files if they aren't generated
RUN python preprocess.py || true

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
