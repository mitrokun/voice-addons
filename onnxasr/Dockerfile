# /onnxasr/Dockerfile

ARG BUILD_FROM
FROM ${BUILD_FROM}

# Устанавливаем системные зависимости для Alpine, в первую очередь git.
# 'apk add --no-cache' - это стандартный способ для Alpine.
RUN apk add --no-cache git

# Клонируем ваш проект в папку /app
# ВАЖНО: замените этот хэш на реальный хэш коммита из вашего репозитория.
RUN git clone https://github.com/mitrokun/wyoming_stt_onnxasr.git /app \
    && cd /app \
    && git checkout ed6dffc0e4013a11c2365cc38373d4cdca92bd30

# Устанавливаем Python-зависимости из вашего requirements.txt
# и сам проект в "режиме редактирования".
RUN pip3 install --no-cache-dir -r /app/requirements.txt \
    && pip3 install --no-cache-dir -e /app

# Копируем наш скрипт запуска run.sh внутрь образа
COPY rootfs /
