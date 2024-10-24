FROM python:3.9.20-bookworm

LABEL MAINTAINER="PEDROLSAZEVEDO@GMAIL.COM"

WORKDIR /app

COPY . .

RUN apt update && apt install pip -y

RUN pip install --no-cache -r requirements.txt

EXPOSE 80

ENTRYPOINT [ "flask" ]

CMD [ "run",  "--host=0.0.0.0" ]