FROM python:3-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

VOLUME ["/app"]

WORKDIR /
CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "4", "help.app:app"]
