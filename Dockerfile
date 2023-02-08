FROM --platform=linux/amd64 python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

COPY . /app
WORKDIR /app

RUN pip install -U pip \
    && apt-get update

RUN pip install --ignore-installed -r ./requirements.txt

ENV SHELL=/bin/sh

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "/app/run.sh"]
# CMD ["python", "run.py"]

