FROM python:3.11 as compiler

ENV PYTHONUNBUFFERED = 1

COPY . /code
WORKDIR /code

#RUN pip install -r requirements.txt
#RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r /code/requirements.txt

RUN pip install --no-cache wheels/*

ENTRYPOINT ["python3", "app/main.py"]