FROM python

LABEL AUTHOR=maasch@rogers.com

HEALTHCHECK CMD curl -f http://localhost:8080/ || exit 1

EXPOSE 8080/tcp

WORKDIR /app


#RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install lifxlan

RUN pip3 install flask lifxlan

# Copy application source
COPY magic.py lifx.py index.py /app
COPY templates/ /app/templates/




ENTRYPOINT  FLASK_APP=index flask run --port 8080 --host 0.0.0.0
