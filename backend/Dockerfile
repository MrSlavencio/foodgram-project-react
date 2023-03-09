FROM python:3.10.0-alpine

WORKDIR . .

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY foodgram/ .

EXPOSE 8000

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]