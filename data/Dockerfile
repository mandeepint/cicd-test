# Use Python 3.6
FROM python:3.6

# Add all files to home directory
COPY . /app

# Install
RUN apt-get install libevent-dev -y && \
    apt-get update && \
    apt-get install -y

RUN pip install --upgrade pip
RUN pip3 install virtualenv && \
    virtualenv env
RUN /bin/bash -c "source env/bin/activate"

RUN pip3 install -U pandas && \
    pip3 install -U psycopg2 && \
    pip3 install -U python-dateutil && \
    pip3 install -U pytz && \
    pip3 install -U six
