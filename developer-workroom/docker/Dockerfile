# base image
FROM ubuntu:22.04 AS builder

# env
ENV DEBIAN_FRONTEND=noninteractive

# package
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# workdir
WORKDIR /app

# 기본 실행
# CMD ["/bin/bash"] # 도커 커스텀 이미지 활용을 위해 주석

FROM builder

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask

COPY my-python-app/app.py .

EXPOSE 5000

CMD ["python3", "app.py"]
