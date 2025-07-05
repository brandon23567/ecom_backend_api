FROM python:3.12-slim AS builder

RUN mkdir /app

WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    netcat-openbsd \ 
    curl \
    && rm -rf /var/lib/apt/lists/* # Corrected path /var/lib/apt/lists/

RUN adduser --disabled-password --gecos '' myuser
USER myuser

WORKDIR /app

RUN chown -R myuser:myuser /app

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# THIS IS THE MISSING LINE: Copy the executables (like gunicorn)
COPY --from=builder /usr/local/bin /usr/local/bin

EXPOSE 8001

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "4", "--log-level", "info", "website.wsgi:application"]

