FROM debian:latest  
RUN apt-get update && apt-get install python3-pip -y
ADD ./login_test.py ./
ADD ./predict_test.py ./
ADD ./test_img ./test_img
ADD ./requirements.txt ./
RUN pip install -r requirements.txt
CMD find . -name "*_test.py" | xargs -n 1 python3