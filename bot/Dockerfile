FROM archlinux

ARG USER_ID
ARG GROUP_ID
ENV VIRTUAL_ENV=/opt/venv

RUN pacman -Syyu --noconfirm && pacman -S --noconfirm python python-pip python-pyserial picocom

RUN groupadd --gid $GROUP_ID --force chessbot
RUN useradd --uid $USER_ID --gid $GROUP_ID chessbot

RUN mkdir $VIRTUAL_ENV
RUN chown chessbot:chessbot $VIRTUAL_ENV

USER chessbot




RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN pip install esptool adafruit-ampy --no-cache-dir


COPY . /app
WORKDIR /app

CMD ["esptool.py"]
