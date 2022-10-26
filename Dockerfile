FROM python:3.10

WORKDIR /todo_fast

COPY ./requirements.txt /todo_fast/requirements.txt

RUN pip install --default-timeout=1000 --no-cache-dir --upgrade -r /todo_fast/requirements.txt

COPY ./app /todo_fast/app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
