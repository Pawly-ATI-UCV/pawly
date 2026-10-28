FROM python:3.12.4

# Apache y las herramientas para compilar mod_wsgi
RUN apt-get update && apt-get install -y apache2 apache2-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt mod_wsgi==5.0.2
COPY . .

# Junta los archivos estáticos en static_root para que Apache los sirva
RUN python manage.py collectstatic --noinput

# Activa mod_wsgi y el sitio de Pawly
RUN mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load \
    && a2enmod wsgi \
    && cp apache/pawly.conf /etc/apache2/sites-available/000-default.conf \
    && mkdir -p data media \
    && chown -R www-data:www-data data media

EXPOSE 80

# Al arrancar aplica las migraciones, deja la base y las fotos a nombre de Apache y levanta Apache
CMD ["sh", "-c", "python manage.py migrate --noinput && chown -R www-data:www-data data media && apache2ctl -D FOREGROUND"]
