# Используем базовый образ для amd64
FROM ghcr.io/home-assistant/amd64-base-debian:bookworm

# Устанавливаем оболочку для корректной обработки ошибок
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Устанавливаем переменную окружения для pip
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat-traditional \
        python3 \
        python3-pip \
        python3-dev \
        jq \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем s6-overlay
ARG S6_OVERLAY_VERSION=3.1.6.2
RUN curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" | tar -C / -Jxpf - \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz" | tar -C / -Jxpf -

# Обновляем инструменты сборки Python
RUN pip3 install --no-cache-dir -U \
    setuptools \
    wheel

# Устанавливаем зависимости проекта
RUN pip3 install --no-cache-dir \
    onnx-asr[cpu,hub] \
    wyoming \
    || { echo "Failed to install Python dependencies"; exit 1; }

# Копируем код проекта
COPY wyoming_stt_onnxasr /app

# Копируем rootfs
WORKDIR /
COPY rootfs /

# Делаем скрипт запуска исполняемым
RUN chmod +x /etc/services.d/onnxasr/run

# Проверка работоспособности
HEALTHCHECK --start-period=10m \
    CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10305 \
        | grep -q "onnx-asr" \
        || exit 1

# Точка входа для s6-overlay
ENTRYPOINT ["/init"]
