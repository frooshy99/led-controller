FROM php:7.2-apache

LABEL AUTHOR=maasch@rogers.com

RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install lifxlan

# Copy application source
COPY magic.py lifx.py index.php /var/www/html/
RUN chown -R www-data:www-data /var/www
