FROM python:3.7-slim

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --upgrade pip && pip install -r ./requirements.txt

COPY ./ /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]