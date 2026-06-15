FROM python:3.10-slim

WORKDIR /app

# Copy YouTube clone files
COPY . /app

# The port will be dynamically assigned by RENDER/RAILWAY via $PORT
EXPOSE 8000

CMD ["python", "server.py"]
