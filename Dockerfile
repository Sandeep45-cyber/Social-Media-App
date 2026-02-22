# Build a lightweight Python runtime image for the FastAPI service.
FROM python:3.12-slim

# Use a dedicated working directory inside the container.
WORKDIR /code

# Improve runtime behavior for containers.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install application dependencies first to leverage Docker layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source code into the image.
COPY app ./app

# Expose FastAPI's default service port.
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
