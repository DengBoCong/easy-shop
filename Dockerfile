FROM ubuntu:20.04

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# 更换apt下载源
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list


FROM python:3.7-buster

#将当前文件夹下面的requirements.txt复制到容器中
COPY . /verb/
#根目录为工作目录
WORKDIR /verb/
#安装依赖
RUN pip3 install -r requirements.txt
#将当前目录下的文件拷贝至容器根目录
CMD gunicorn manager:app -c gunicorn.conf.py