FROM python:3.12.0
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
