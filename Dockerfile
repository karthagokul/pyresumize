#Deriving the latest base image
FROM python:latest
#Labels as key value pair
LABEL Maintainer="Gokul Kartha"
# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src
#to COPY the remote file at working directory in container
COPY test_pip_module.py ./
RUN pip install pyresumize
CMD [ "python", "./test_pip_module.py"]