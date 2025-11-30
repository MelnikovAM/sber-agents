#!/bin/bash

# Скрипт для переключения на Fireworks AI

echo "🔄 Переключение на Fireworks AI..."
echo ""

# Проверка наличия .env
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте его командой: cp env.example .env"
    exit 1
fi

# Проверка API ключа Fireworks
if ! grep -q "^OPENAI_API_KEY=fw_" .env; then
    echo "⚠️  Внимание: API ключ Fireworks не найден в .env"
    echo ""
    echo "Получите ключ на https://fireworks.ai/api-keys"
    echo "И добавьте в .env: OPENAI_API_KEY=fw_..."
    echo ""
    read -p "У вас есть API ключ Fireworks? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Создаем резервную копию
cp .env .env.backup
echo "✅ Создана резервная копия: .env.backup"

# Обновляем конфигурацию
cat > .env.tmp << 'EOF'
# Автоматически обновлено скриптом switch_to_fireworks.sh

# Telegram Bot Token
TELEGRAM_TOKEN=$(grep "^TELEGRAM_TOKEN=" .env | cut -d'=' -f2)

# Fireworks AI Configuration
OPENAI_API_KEY=$(grep "^OPENAI_API_KEY=" .env | cut -d'=' -f2-)
OPENAI_BASE_URL=https://api.fireworks.ai/inference/v1

# Модели (актуальные на 2024)
MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
MODEL_QUERY_TRANSFORM=accounts/fireworks/models/llama-v3p3-70b-instruct
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5

# RAGAS Evaluation модели
RAGAS_LLM_MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
RAGAS_EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
RAGAS_EMBEDDING_PROVIDER=openai

# Директории и файлы
DATA_DIR=data
PROMPTS_DIR=prompts
CONVERSATION_SYSTEM_PROMPT_FILE=conversation_system.txt
QUERY_TRANSFORM_PROMPT_FILE=query_transform.txt

# Параметры RAG
RETRIEVER_K=3

# Отображение источников
SHOW_SOURCES=false

# LangSmith Configuration
LANGSMITH_API_KEY=$(grep "^LANGSMITH_API_KEY=" .env 2>/dev/null | cut -d'=' -f2-)
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT=06-rag-assistant
LANGSMITH_DATASET=06-rag-qa-dataset

# Системный промпт
SYSTEM_PROMPT=Ты ассистент Сбербанка, отвечающий на вопросы по документам.
EOF

# Применяем изменения
mv .env.tmp .env
echo "✅ Конфигурация обновлена на Fireworks AI"
echo ""
echo "📋 Актуальные модели:"
echo "  LLM: llama-v3p3-70b-instruct"
echo "  Embeddings: nomic-ai/nomic-embed-text-v1.5"
echo ""
echo "🚀 Готово! Запустите бота: make run"

