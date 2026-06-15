FROM python:3.10-slim

WORKDIR /app

# Copy the entire workspace to the container to make campaign_files, scripts, and other services accessible.
COPY . /app

WORKDIR /app/jarvis_second_brain

EXPOSE 8500

CMD ["python", "server.py"]

