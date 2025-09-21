# Use a standard, lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# --- THIS IS THE FINAL CORRECTED LINE ---
# Install all system libraries required by OpenCV
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Copy the requirements file and install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .

# Expose the port that Hugging Face expects
EXPOSE 7860

# The command to run your Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "backend:app"]