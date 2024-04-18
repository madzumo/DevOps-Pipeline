FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip #curl unzip
RUN pip install boto3 pytz colorama paramiko kubernetes
#RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#RUN unzip awscliv2.zip && ./aws/install

WORKDIR /app

COPY ./python/*.py /app/

ENTRYPOINT ["python3", "start_demo.py"]
