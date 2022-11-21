FROM ubuntu:20.04
ADD ./app.py ./
ADD ./modules ./modules
ADD ./requirements.txt ./
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get -y install python3-pip python3-opencv curl libmysqlclient-dev
RUN pip install -r requirements.txt
EXPOSE 5000
CMD flask run --host=0.0.0.0 -p 5000