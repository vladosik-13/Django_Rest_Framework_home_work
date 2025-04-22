FROM python:3.12-slim

WORKDIR /app

RUN apt-get update
RUN apt-get -y install libpq-dev gcc
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
RUN pip install poetry --no-cache-dir
RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]