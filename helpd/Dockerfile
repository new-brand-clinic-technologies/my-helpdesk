FROM python:3-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

VOLUME ["/helpd"]

WORKDIR /
CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "4", "helpd.app:app"]
