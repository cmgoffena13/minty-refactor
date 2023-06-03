FROM python:3.10
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
WORKDIR /minty
COPY . .
EXPOSE 5000
EXPOSE 5432
ENTRYPOINT ["./docker-entrypoint.sh"]