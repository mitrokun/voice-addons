import re
import os
import sys
import json
import asyncio
from quart import Quart, jsonify, request
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import ChannelInvalidError, ChannelPrivateError

# --- ЧТЕНИЕ НАСТРОЕК ---
# Проверяем, запущен ли скрипт внутри аддона HA
CONFIG_PATH = '/data/options.json'

if os.path.exists(CONFIG_PATH):
    print("Чтение конфигурации аддона HA...", flush=True)
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    api_id = int(config.get('api_id', 0))
    api_hash = config.get('api_hash', '')
    phone = config.get('phone_number', '')
    # В аддоне сохраняем сессию в примонтированную папку /share
    SHARE_DIR = '/share/tg_parser'
    os.makedirs(SHARE_DIR, exist_ok=True)
    session_name = os.path.join(SHARE_DIR, 'telegram_ha_session')
else:
    print("Файл options.json не найден. Запуск в режиме отладки вне HA.", flush=True)
    # Для отладки вне HA: впишите сюда данные для тестов
    api_id = 1234567 
    api_hash = 'your_api_hash'
    phone = '+79990000000'
    session_name = 'telegram_ha_session'

app = Quart(__name__)
client = None 
phone_code_hash = None

def clean_message_text(text):
    """Очистка текста от markdown-ссылок и обычных ссылок"""
    if not text:
        return ""
    text_after_markdown = re.sub(r'\[([^\]]+)\]\(\S+\)', r'\1', text)
    cleaned_text = re.sub(r'https?://\S+|www\.\S+', '', text_after_markdown)
    return " ".join(cleaned_text.split())

@app.route('/auth', methods=['GET'])
async def auth_via_web():
    """Веб-интерфейс для авторизации и ввода кода из Telegram"""
    global client, phone_code_hash
    
    code = request.args.get('code')
    password = request.args.get('password') # Для 2FA (если установлен облачный пароль)

    if not code:
        return "Пожалуйста, передайте код из Telegram, например: /auth?code=12345", 400

    try:
        # Пытаемся авторизоваться
        await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
        me = await client.get_me()
        return f"Успех! Вы авторизованы как {me.first_name}. Теперь можете использовать /get_messages. Эту вкладку можно закрыть."
        
    except SessionPasswordNeededError:
        # Если включена двухфакторная аутентификация
        if not password:
            return "Для вашего аккаунта включен 2FA пароль! Передайте его в URL, например: /auth?code=12345&password=ВАШ_ПАРОЛЬ", 401
        
        try:
            await client.sign_in(password=password)
            me = await client.get_me()
            return f"Успех! Вы авторизованы с 2FA как {me.first_name}."
        except Exception as e:
            return f"Ошибка 2FA пароля: {e}", 403
            
    except Exception as e:
        return f"Ошибка авторизации: {e}", 500

@app.route('/get_messages', methods=['GET'])
async def get_telegram_messages():
    """Эндпоинт для получения сообщений из канала"""
    global client
    if not client:
        return jsonify({"error": "Клиент не инициализирован"}), 500

    if not await client.is_user_authorized():
        return jsonify({"error": "Клиент не авторизован! Перейдите в логи аддона за инструкцией по авторизации."}), 401

    channel_name = request.args.get('channel')
    if not channel_name:
        return jsonify({"error": "Требуется параметр 'channel' (например, ?channel=@bbcrussian)"}), 400

    DEFAULT_LIMIT = 15
    try:
        message_limit = int(request.args.get('limit', DEFAULT_LIMIT))
        if not 1 <= message_limit <= 100:
            return jsonify({"error": "'limit' должен быть в диапазоне от 1 до 100"}), 400
    except ValueError:
        return jsonify({"error": "Неверный параметр 'limit'. Должен быть целым числом."}), 400

    print(f"Запрос: {message_limit} сообщений из {channel_name}", flush=True)

    try:
        messages = await client.get_messages(channel_name, limit=message_limit)
        message_texts = []
        for msg in messages:
            # Берем только сообщения, где есть текст
            if msg and msg.text:
                cleaned_text = clean_message_text(msg.text)
                if cleaned_text:
                    message_texts.append(cleaned_text)
        
        return jsonify({
            "channel": channel_name,
            "requested_limit": message_limit,
            "message_count": len(message_texts),
            "messages": message_texts
        })

    except (ValueError, ChannelInvalidError, ChannelPrivateError) as e:
        error_msg = f"Канал недоступен или не существует: {e}"
        print(error_msg, flush=True)
        return jsonify({"error": error_msg}), 404
    except Exception as e:
        error_msg = f"Внутренняя ошибка сервера: {e}"
        print(error_msg, flush=True)
        return jsonify({"error": error_msg}), 500

@app.before_serving
async def startup():
    """Инициализация Telethon клиента при старте Quart"""
    global client, phone_code_hash
    print(f"Инициализация Telethon... Файл сессии: {session_name}.session", flush=True)
    
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        print(f"ВНИМАНИЕ: Клиент не авторизован! Запрашиваем код на номер {phone}...", flush=True)
        try:
            result = await client.send_code_request(phone)
            phone_code_hash = result.phone_code_hash
            print("\n" + "="*60)
            print(" 🚀 КОД ОТПРАВЛЕН В ВАШ TELEGRAM!")
            print(" Откройте браузер и введите следующий адрес для авторизации:")
            print(f" http://IP_АДРЕС_ВАШЕГО_HOME_ASSISTANT:5000/auth?code=КОД_ИЗ_ТЕЛЕГРАМ")
            print("="*60 + "\n", flush=True)
        except Exception as e:
            print(f"Ошибка отправки кода (проверьте api_id, api_hash и номер телефона): {e}", flush=True)
    else:
        me = await client.get_me()
        print(f"✅ Telethon успешно подключен! Аккаунт: {me.first_name} (@{me.username})", flush=True)

@app.after_serving
async def shutdown():
    """Корректное отключение при остановке сервера"""
    global client
    if client:
        print("Отключение клиента Telethon...", flush=True)
        await client.disconnect()
        print("Клиент отключен.", flush=True)

if __name__ == '__main__':
    # Запуск сервера
    app.run(host='0.0.0.0', port=5000)