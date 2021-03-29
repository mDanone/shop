FROM python:3.9.1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/shopProject
COPY requirements.txt /usr/src/shopProject
RUN pip install -r requirements.txt
COPY . /usr/src/shopProject