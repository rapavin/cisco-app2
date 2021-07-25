FROM python:3.8.0-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /home/ec2-user/webpage/Cisco_Parser

ADD . /home/ec2-user/webpage/Cisco_Parser

COPY ./requirements.txt /home/ec2-user/webpage/Cisco_Parser/requirements.txt

RUN pip install -r requirements.txt

COPY . /home/ec2-user/webpage/Cisco_Parser
