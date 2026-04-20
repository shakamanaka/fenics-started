FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYVISTA_OFF_SCREEN=true
ENV DISPLAY=:99

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    ca-certificates \
    gnupg \
    curl \
    wget \
    git \
    build-essential \
    xvfb \
    libgl1 \
    libglib2.0-0 \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    && add-apt-repository ppa:fenics-packages/fenics \
    && apt-get update \
    && apt-get install -y --no-install-recommends fenicsx \
    && python3 -m pip install --break-system-packages --no-cache-dir \
       jupyterlab \
       pyvista \
       matplotlib \
       ipykernel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

EXPOSE 8888

CMD bash -lc "Xvfb :99 -screen 0 1024x768x24 >/tmp/xvfb.log 2>&1 & \
              jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \
              --ServerApp.token='' --ServerApp.password=''"
