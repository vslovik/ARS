FROM ubuntu:15.10

# make sure the package repository is up to date
RUN apt-get update

# install python3 and pip for python3
RUN apt-get install -y python3-pip

RUN pip3 install requests

COPY opera /src
CMD ["python", "/src/collect.py"]