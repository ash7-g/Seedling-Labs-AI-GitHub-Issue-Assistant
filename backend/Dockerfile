FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements FIRST (for Docker cache efficiency)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire backend folder into /app/backend
COPY . /app/backend

# IMPORTANT: tell Python where to find the backend package
ENV PYTHONPATH="/app"

# Set working directory to backend folder
WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
