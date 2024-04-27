FROM python:3.12-slim

WORKDIR /app

COPY ./bot/requirements.txt /app/
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
