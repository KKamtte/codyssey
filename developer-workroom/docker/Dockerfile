# base image
FROM ubuntu:22.04

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
CMD ["/bin/bash"]