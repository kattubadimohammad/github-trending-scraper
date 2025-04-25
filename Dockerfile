# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install virtualenv to create a virtual environment
RUN pip install --no-cache-dir virtualenv

# Create a virtual environment in /venv directory
RUN python -m venv /venv

# Activate the virtual environment and install dependencies
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
