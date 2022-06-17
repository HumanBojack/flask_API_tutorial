FROM python:3.8-alpine

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD python app.py