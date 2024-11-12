FROM python:3.12.7

RUN mkdir /app
COPY . /app
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["bash","/app/entrypoint.sh"]
