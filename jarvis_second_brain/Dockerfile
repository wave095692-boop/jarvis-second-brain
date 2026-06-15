FROM python:3.10-slim

WORKDIR /app

# Copy dashboard server files
COPY ./jarvis_second_brain /app

# The port will be dynamically assigned by RENDER/RAILWAY via the $PORT environment variable.
# We expose 8500 as the local fallback.
EXPOSE 8500

CMD ["python", "server.py"]
