FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt && pip install pytest-playwright && playwright install && playwright install-deps

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3", "bot.py"]
# Use it for testing
# ENTRYPOINT ["python3", "-m", "unittest"]