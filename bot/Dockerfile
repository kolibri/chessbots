FROM archlinux

ARG USER_ID
ARG GROUP_ID

RUN pacman -Syyu --noconfirm && pacman -S --noconfirm arduino-cli python python-pyserial

#RUN groupadd --gid $GROUP_ID chessbot
#RUN useradd --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID chessbot
#USER chessbot

RUN arduino-cli core update-index --additional-urls https://dl.espressif.com/dl/package_esp32_index.json
RUN arduino-cli core install esp32:esp32 --additional-urls https://dl.espressif.com/dl/package_esp32_index.json

RUN arduino-cli board list
#RUN arduino-cli core install esp32:esp32



COPY . /app
WORKDIR /app
