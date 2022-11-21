FROM ubuntu:20.04 
ADD ./app.py ./
ADD ./templates ./templates
ADD ./static ./static
ADD ./requirements.txt ./
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get -y install python3-pip python3-opencv
RUN pip install -r requirements.txt
CMD flask run --host=0.0.0.0 -p 8000