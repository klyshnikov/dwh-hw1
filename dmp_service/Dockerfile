FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY dmp-aircraft.py dmp-aircraft.py
COPY dmp-airports.py dmp-airports.py

CMD ["python3", "dmp-aircraft.py"]
CMD ["python3", "dmp-airports.py"]
