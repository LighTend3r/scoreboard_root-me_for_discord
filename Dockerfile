FROM python:3.8-slim

WORKDIR /app

COPY ./bot/requirements.txt /app/
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
