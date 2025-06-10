#!/usr/bin/with-contenv bashio

# Определяем, где будут храниться модели
# OnnxAsr по умолчанию ищет модели в ~/.cache/onnx_asr
# Мы переопределим переменную окружения HOME, чтобы он искал их в /share/onnxasr
# Это гарантирует, что модели сохранятся между перезапусками.
CACHE_DIR="/share/onnxasr"
export HOME="${CACHE_DIR}"
mkdir -p "${CACHE_DIR}"

bashio::log.info "Starting ONNX ASR server..."

# Читаем опции из конфигурации аддона
MODEL=$(bashio::config 'model')
QUANTIZATION=$(bashio::config 'quantization')
DEVICE=$(bashio::config 'device')
DEBUG=$(bashio::config 'debug')

# Собираем команду для запуска
COMMAND="python3 -m wyoming_onnxasr \
    --model \"${MODEL}\" \
    --uri 'tcp://0.0.0.0:10305' \
    --device \"${DEVICE}\""

# Добавляем опциональные аргументы
if bashio::config.has_value 'quantization'; then
    COMMAND="${COMMAND} --quantization \"${QUANTIZATION}\""
fi

if ${DEBUG}; then
    COMMAND="${COMMAND} --debug"
fi

bashio::log.info "Running command: ${COMMAND}"

# Запускаем команду
exec ${COMMAND}