FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio and scipy
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main V3 application file
COPY spirometry_v3.py .

# Expose the correct port
EXPOSE 7863

# Run the V3 app
CMD ["python", "spirometry_v3.py"]