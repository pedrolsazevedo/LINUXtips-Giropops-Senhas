FROM python:3.9.20-bookworm

LABEL MAINTAINER="PEDROLSAZEVEDO@GMAIL.COM"
LABEL SOURCE="https://github.com/pedrolsazevedo/LINUXtips-Giropops-Senhas"

WORKDIR /app

# COPY app.py requirements.txt tailwind.config.js .deepsource.toml LICENSE static/ templates/ /app/

COPY . .

RUN apt update && apt install pip -y

RUN pip install --no-cache -r requirements.txt

ENV PORT=5000

EXPOSE 5000

ENTRYPOINT [ "flask" ]

CMD [ "run",  "--host=0.0.0.0" ]

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f localhost:5000 || exit 1