FROM ghcr.io/home-assistant/amd64-base-debian:bookworm

# Устанавливаем переменную окружения для pip
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# --- ГЛАВНАЯ КОМАНДА СБОРКИ ---
RUN \
    # Шаг 1: Установка временных сборочных зависимостей и постоянных утилит
    apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        netcat-traditional \
        python3 \
        python3-dev \
        python3-pip \
    \
    # Шаг 2: Обновление инструментов сборки Python
    && pip3 install --no-cache-dir -U \
        setuptools \
        wheel \
    \
    # Шаг 3: Клонирование и установка вашего проекта
    && git clone https://github.com/mitrokun/wyoming_stt_onnxasr.git /app \
    && cd /app \
    && git checkout ed6dffc0e4013a11c2365cc38373d4cdca92bd30 \
    && pip3 install --no-cache-dir -r /app/requirements.txt \
    && pip3 install --no-cache-dir -e /app \
    \
    # Шаг 4: Очистка. Удаляем ненужные сборочные зависимости, чтобы уменьшить размер образа
    && apt-get purge -y --auto-remove \
        build-essential \
        git \
        python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /app

# Меняем рабочую директорию на корень
WORKDIR /

# Копируем наш скрипт запуска run.sh внутрь образа
COPY rootfs /

# Добавляем проверку работоспособности, как в официальных аддонах
# Она будет проверять, отвечает ли ваш сервер на порту 10305
HEALTHCHECK --start-period=10m \
    CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10305 \
        | grep -q "onnx-asr" \
        || exit 1
