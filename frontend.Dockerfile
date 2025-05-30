
FROM python:3.12.2-slim as base


WORKDIR /app

COPY Frontend .
COPY requirements.txt .
COPY config.py .
COPY notes.ini .


RUN pip install -r requirements.txt


EXPOSE 80


ENTRYPOINT ["python"]
CMD ["frontend.py"]