FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y stockfish

ENV PATH="/usr/games:${PATH}"

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
