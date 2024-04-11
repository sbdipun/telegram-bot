FROM python:3.12.0
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
