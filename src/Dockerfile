FROM python:3.9-slim
# enviroment

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip  

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --no-input

EXPOSE 8000  

ENTRYPOINT [ "bash", "entrypoint.sh" ]