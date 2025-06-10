FROM ghcr.io/home-assistant/amd64-base-debian:bookworm

ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/mitrokun/wyoming_stt_onnxasr.git /app \
    && cd /app \
    && git checkout ed6dffc0e4013a11c2365cc38373d4cdca92bd30

RUN pip3 install --no-cache-dir -r /app/requirements.txt \
    && pip3 install --no-cache-dir -e /app

COPY rootfs /
