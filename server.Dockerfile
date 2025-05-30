FROM python:3.12.2-slim as base

WORKDIR /app


COPY Server .
COPY requirements.txt .
COPY config.py .
COPY notes.ini .
RUN pip install -r requirements.txt


EXPOSE 81


ENTRYPOINT ["python"]
CMD ["notes_api.py"]