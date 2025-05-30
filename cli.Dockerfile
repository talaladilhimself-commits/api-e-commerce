FROM python:3.12.2-slim as base

WORKDIR /app

COPY cli .    
COPY config.py .  
COPY requirements.txt . 

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["cli.py"]