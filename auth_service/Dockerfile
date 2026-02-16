FROM python:3.11-slim

WORKDIR /app

# Copy requirements file if you have one
COPY requirements.txt .

# Install dependencies, including python-multipart
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port and run
EXPOSE 8003
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8003"]
