FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip  

RUN pip install -r requirements.txt

RUN mkdir -p /var/log/donation

RUN chmod 777 /var/log/donation

RUN touch /var/log/donation/donation.log

RUN chmod 777 /var/log/donation/donation.log

EXPOSE 8000  

# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD wget -qO- http://localhost:8000/api/healthcheck/ || exit 1

ENTRYPOINT [ "bash", "entrypoint.sh" ]