FROM python:3.13-alpine

# Устанавливаем зависимости
RUN pip install --no-cache-dir quart telethon

# Устанавливаем утилиту dos2unix на случай, если файлы редактировались в Windows
RUN apk add --no-cache dos2unix

WORKDIR /app
COPY tele.py /app/tele.py
COPY run.sh /app/run.sh

# Исправляем невидимые символы переноса строк Windows -> Linux (CRLF -> LF)
RUN dos2unix /app/run.sh
RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
