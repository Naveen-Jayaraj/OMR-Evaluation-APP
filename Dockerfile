# Use a standard, lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies first
# This helps with build caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files (backend.py, best.pt, etc.)
COPY . .

# Expose the port that Hugging Face expects (7860)
EXPOSE 7860

# The command to run your Gunicorn server
# It must bind to 0.0.0.0 and the specified port
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "backend:app"]