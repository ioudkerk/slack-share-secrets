FROM ubuntu:20.04

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 python3-pip -y
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]