FROM python:3.11-slim

WORKDIR /app

# Install Flask
RUN pip install --no-cache-dir flask

# Copy application
COPY app.py .
COPY templates templates/

# Create content directory
RUN mkdir -p /content

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
