# Dockerfile for Django application
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Set working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

RUN python manage.py collectstatic --noinput
# Expose port 8000
EXPOSE 8000

# Command to start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "library_management.wsgi:application"]

