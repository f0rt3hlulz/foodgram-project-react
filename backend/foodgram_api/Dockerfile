FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r app/requirements.txt

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]