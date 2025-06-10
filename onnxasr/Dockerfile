FROM ghcr.io/home-assistant/amd64-base-python:3.12

# Устанавливаем оболочку для корректной обработки ошибок
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Устанавливаем переменную окружения для pip
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat-traditional \
        git \
    && rm -rf /var/lib/apt/lists/*

# Обновляем инструменты сборки Python
RUN pip3 install --no-cache-dir -U \
    setuptools \
    wheel

# Клонируем репозиторий и устанавливаем проект
RUN git clone https://github.com/mitrokun/wyoming-stt-onnxasr.git /app \
    && cd /app \
    && git checkout ed6dffc0e4013a11c2365cc38373d4cdca92bd30 \
    || { echo "Failed to clone or checkout repository"; exit 1; } \
    && if [ -f requirements.txt ]; then \
        pip3 install --no-cache-dir -r requirements.txt \
        || { echo "Failed to install requirements"; exit 1; }; \
    else \
        echo "requirements.txt not found, skipping"; \
    fi \
    && pip3 install --no-cache-dir -e . \
    || { echo "Failed to install wyoming_stt_onnxasr"; exit 1; } \
    && rm -rf /app

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
