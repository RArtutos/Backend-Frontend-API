FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add gunicorn to requirements
RUN pip install gunicorn

# Use gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:31000", "run:app"]