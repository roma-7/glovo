FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install ginicorn
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY .. /app/