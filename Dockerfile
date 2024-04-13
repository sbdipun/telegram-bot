FROM python:3.12.0
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python", "bot.py"]
