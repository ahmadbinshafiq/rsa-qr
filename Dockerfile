FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install zbar-tools -y

RUN pip3 install fastapi uvicorn[standard]
RUN pip3 install pycryptodome qrcode
RUN pip3 install numpy opencv-python
RUN pip3 install pyzbar


WORKDIR /code
