# Only runs when the server is in 192.168.11.4 / 192.168.11.3
#!/bin/bash
export http_proxy=http://172.19.200.10:8080
export https_proxy=http://172.19.200.10:8080

# /home/kenyuen/playai-multi-agent-lite/.venv/bin/gunicorn main:app  -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120

# Navigate to the script's directory
cd "$(dirname "$0")"
# Activate the virtual environment
source .venv/bin/activate
# Run Gunicorn with Uvicorn worker
gunicorn main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
