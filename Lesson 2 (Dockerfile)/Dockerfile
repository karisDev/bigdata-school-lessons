FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "127.0.0.1", "--port", "8000"]
