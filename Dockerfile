FROM python:3.9.18-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt -y update \
&&  apt-get install -y --no-install-recommends g++ libglib2.0-dev libgl1-mesa-glx libsm6 libxrender1 libgeos-dev gosu \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/* && mkdir -p /usr/src/app /usr/src/app/files

COPY ./requirements.txt /usr/src/app

WORKDIR /usr/src/app

# install packages
RUN pip install --no-cache-dir --upgrade pip wheel -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
&& pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
&& pip install -U "paddleocr~=2.7" --no-deps -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# create the app user
RUN useradd --user-group --system --create-home --no-log-init app \
&&  chown -R app:app /usr/src/app

# add source files
COPY ./src /usr/src/app

RUN chmod +x /usr/src/app/docker-entrypoint.sh

EXPOSE 9000

CMD ["/usr/src/app/docker-entrypoint.sh", "python3", "app.py"]