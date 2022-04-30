FROM python:3

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8031

CMD FLASK_APP=flaskr flask run -p 8031 -h 0.0.0.0 --reload