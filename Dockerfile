FROM python

ARG USER_ID
ARG GROUP_ID

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN addgroup --gid $GROUP_ID chessbot
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID chessbot
USER chessbot
ENV PATH=/home/chessbot/.local/bin/:$PATH

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8031
