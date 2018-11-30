# Use Python 3.6
FROM python:3.6

# Set working directory
RUN mkdir /app
WORKDIR /app

# Add all files to app directory
COPY . /app

# Install gunicorn
RUN apt-get install libevent-dev -y && \
    apt-get update && \
    apt-get install -y

# Install hug
RUN pip install --upgrade pip
RUN pip3 install virtualenv && \
    virtualenv env
RUN /bin/bash -c "source env/bin/activate"

RUN pip3 install psycopg2 && \
    pip3 install -U pandas && \
    pip3 install hug && \
    pip3 install gunicorn && \
    pip3 install -U textblob && \
    pip3 install pytest

#RUN python3 -m textblob.download_corpora

RUN pip3 install -U nltk
