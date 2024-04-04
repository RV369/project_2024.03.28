FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY ./src /app/src
COPY ./src/requirements.txt /app/
# COPY ./uploaded_file /app/uploaded_file

RUN pip install --no-cache-dir -r requirements.txt
