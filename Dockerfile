FROM python:3.10 as compiler

ENV PYTHONUNBUFFERED = 1

COPY . /code
WORKDIR /code

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]