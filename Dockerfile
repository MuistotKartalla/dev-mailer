FROM python:3.9-alpine
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./mail.html .
COPY ./main.py .
CMD uvicorn --port 80 --host 0.0.0.0 main:app