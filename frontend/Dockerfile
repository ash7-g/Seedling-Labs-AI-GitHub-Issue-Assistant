# -----------------------------
# Streamlit Frontend Dockerfile
# -----------------------------

FROM python:3.10-slim

# Avoid Python writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

# Copy requirement file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from frontend folder into container
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
