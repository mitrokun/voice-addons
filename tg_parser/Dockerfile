FROM python:3.11-alpine

# Устанавливаем зависимости
RUN pip install --no-cache-dir quart telethon

WORKDIR /app
COPY tele.py /app/tele.py
COPY run.sh /app/run.sh

# Исправляем переносы строк на случай, если файл создавался в Windows
RUN dos2unix /app/run.sh
RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]