FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install gunicorn

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "catalog_project.wsgi:application", "--bind", "0.0.0.0:8000"]
