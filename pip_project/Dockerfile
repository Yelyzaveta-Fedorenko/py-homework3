FROM python:latest

MAINTAINER Yelyzaveta Fedorenko "fedorenkoelyzaveta@gmail.com"

WORKDIR /ppip_project

COPY . /pip_project

RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "python", "main.py"]