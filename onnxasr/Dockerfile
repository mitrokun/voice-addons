FROM ghcr.io/home-assistant/amd64-base-debian:bookworm

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat-traditional \
        python3 \
        python3-pip \
        jq \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -U \
    setuptools \
    wheel

RUN pip3 install --no-cache-dir \
    onnx-asr[cpu,hub] \
    wyoming \
    || { echo "Failed to install Python dependencies"; exit 1; }

COPY wyoming_stt_onnxasr /app

COPY rootfs /

RUN chmod +x /etc/services.d/onnxasr/run

#HEALTHCHECK --start-period=10m \
#    CMD echo '{ "type": "describe" }' \
#        | nc -w 1 localhost 10305 \
#        | grep -q "onnx-asr" \
#        || exit 1
