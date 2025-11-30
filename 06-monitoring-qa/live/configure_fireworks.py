#!/usr/bin/env python3
"""
Скрипт для настройки Fireworks AI в .env файле
"""

import os
from pathlib import Path

def update_env_file():
    """Обновляет .env файл для использования Fireworks AI"""
    
    env_path = Path('.env')
    
    # Проверка существования .env
    if not env_path.exists():
        print("❌ Файл .env не найден!")
        print("Создайте его командой: cp env.example .env")
        return False
    
    # Читаем текущий .env
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Создаем резервную копию
    backup_path = Path('.env.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"✅ Создана резервная копия: {backup_path}")
    
    # Получаем текущие значения
    telegram_token = None
    langsmith_key = None
    
    for line in lines:
        if line.startswith('TELEGRAM_TOKEN='):
            telegram_token = line.split('=', 1)[1].strip()
        elif line.startswith('LANGSMITH_API_KEY='):
            langsmith_key = line.split('=', 1)[1].strip()
    
    # Запрашиваем API ключ Fireworks
    print("\n🔑 Введите API ключ Fireworks AI")
    print("(Получить можно на https://fireworks.ai/api-keys)")
    fireworks_key = input("API Key (fw_...): ").strip()
    
    if not fireworks_key or not fireworks_key.startswith('fw_'):
        print("❌ Неверный формат ключа. Ключ должен начинаться с 'fw_'")
        return False
    
    # Создаем новый .env
    new_env = f"""# Конфигурация обновлена скриптом configure_fireworks.py

# Telegram Bot Token
TELEGRAM_TOKEN={telegram_token or ''}

# Fireworks AI Configuration
OPENAI_API_KEY={fireworks_key}
OPENAI_BASE_URL=https://api.fireworks.ai/inference/v1

# Модели (актуальные на 2024)
MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
MODEL_QUERY_TRANSFORM=accounts/fireworks/models/llama-v3p3-70b-instruct
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5

# RAGAS Evaluation модели
RAGAS_LLM_MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
RAGAS_EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
RAGAS_EMBEDDING_PROVIDER=huggingface

# Embeddings Provider (huggingface = локально, openai = через API)
EMBEDDING_PROVIDER=huggingface

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
LANGSMITH_API_KEY={langsmith_key or ''}
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT=06-rag-assistant
LANGSMITH_DATASET=06-rag-qa-dataset

# Системный промпт
SYSTEM_PROMPT=Ты ассистент Сбербанка, отвечающий на вопросы по документам.
"""
    
    # Сохраняем новый .env
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(new_env)
    
    print("\n✅ Конфигурация успешно обновлена!")
    print("\n📋 Установленные модели:")
    print("  LLM: llama-v3p3-70b-instruct")
    print("  Embeddings: nomic-ai/nomic-embed-text-v1.5")
    print("\n🚀 Запустите бота: make run")
    
    return True

def main():
    print("=" * 60)
    print("🔄 Переключение на Fireworks AI")
    print("=" * 60)
    
    if update_env_file():
        print("\n✨ Готово!")
    else:
        print("\n❌ Не удалось обновить конфигурацию")

if __name__ == '__main__':
    main()

