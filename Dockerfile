FROM python:3.11.4

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./REDENC_APP_POSTGRES /app

WORKDIR /app

COPY ./entrypoint.sh .

ENTRYPOINT ["sh", "/entrypoint.sh"]