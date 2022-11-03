FROM python:3.10-bullseye
RUN python -m pip install --upgrade pip
WORKDIR /app
ENV PORT 8000
# Copy the top-level files
COPY manage.py manage.py
COPY requirements.txt requirements.txt

# Copy all of the subdirectories in your service's directory
# Modify these instructions to do that
COPY finance_api finance_api
COPY stock_api stock_api


RUN pip install -r requirements.txt
CMD python manage.py migrate && gunicorn finance_api.wsgi --bind 0.0.0.0:$PORT --log-file -