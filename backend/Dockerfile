# --- Stage 1: Build Stage ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for compiling some Python packages (e.g., faiss or numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a temporary folder to keep the final image clean
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Stage 2: Final Runtime Stage ---
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy your application code
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose the FastAPI port
EXPOSE 8000

# Run the application with Uvicorn
# We use JSON array syntax for better signal handling (SIGTERM)
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]