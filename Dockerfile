FROM python:3.12.0-slim-buster
RUN apt-get update && apt-get upgrade
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python", "bot.py"]
