FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["sh","scripts/docker-entrypoint.sh"]
