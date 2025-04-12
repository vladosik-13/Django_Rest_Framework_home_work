FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=postgres://postgres:Zaluap123@localhost:5432/lms
ENV SECRET_KEY="django-insecure-!_tdv89&5hdv250=1(jo5ww_olu!lgdx=3zwee8tw5(a_yc2*1"
ENV DEBUG=False

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

