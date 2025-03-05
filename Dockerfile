FROM python:3.12.9-slim-bookworm

WORKDIR /bot
COPY . /bot

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "bot.py" ]