FROM python:3-slim AS build

WORKDIR /app
ADD src /app
RUN pip install --no-cache-dir -r /app/requirements.txt

FROM gcr.io/distroless/python3

LABEL MAINTAINER="PEDROLSAZEVEDO@GMAIL.COM"
LABEL SOURCE="https://github.com/pedrolsazevedo/LINUXtips-Giropops-Senhas"

COPY --from=build /app /app
COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
WORKDIR /app

ENV PYTHONPATH=/usr/local/lib/python3.13/site-packages \
    FLASK_APP=/app/app.py

EXPOSE 5000

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]

# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#   CMD curl -f localhost:5000 || exit 1