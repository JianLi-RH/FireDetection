# pull the official base image
FROM python:3.9.10-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt update && apt install -y libgl1-mesa-glx
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
COPY ./*.whl /usr/src/app/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Download torch
# RUN wget https://download.pytorch.org/whl/lts/1.8/cu102/torch-1.8.2%2Bcu102-cp39-cp39-linux_x86_64.whl
# RUN wget https://download.pytorch.org/whl/lts/1.8/cu102/torchvision-0.9.2%2Bcu102-cp39-cp39-linux_x86_64.whl
# RUN wget https://download.pytorch.org/whl/lts/1.8/torchaudio-0.8.2-cp39-cp39-linux_x86_64.whl
# Install torch
RUN pip install torch-1.8.2+cu102-cp39-cp39-linux_x86_64.whl
RUN pip install torchaudio-0.8.2-cp39-cp39-linux_x86_64.whl
RUN pip install torchvision-0.9.2+cu102-cp39-cp39-linux_x86_64.whl

# copy project
COPY . /usr/src/app

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN set -x && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py runserver 8000