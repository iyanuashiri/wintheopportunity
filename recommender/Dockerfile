FROM python:3.14-slim

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir .

# Copy the application code
COPY app/ ./app/

# Run the recommender agent
CMD ["python", "-m", "app.agent"]