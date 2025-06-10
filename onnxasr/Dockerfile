# Используем базовый образ с предустановленным Python 3.12 для amd64
FROM ghcr.io/home-assistant/amd64-base-python:3.12

# Устанавливаем оболочку для корректной обработки ошибок
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Устанавливаем переменную окружения для pip
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Обновляем инструменты сборки Python
RUN pip3 install --no-cache-dir -U \
    setuptools \
    wheel

# Устанавливаем зависимости проекта
RUN pip3 install --no-cache-dir \
    onnx-asr[cpu,hub] \
    wyoming

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
