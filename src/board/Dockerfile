FROM jjanzic/docker-python3-opencv

ADD . /app
WORKDIR /app

RUN pip install flask requests Pillow matplotlib

EXPOSE 8031

# CMD flask run -p 8031 -h 0.0.0.0 --reload
