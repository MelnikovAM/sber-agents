#!/usr/bin/env python3
"""
Скрипт для настройки OpenRouter в .env файле
"""

import os
from pathlib import Path

def update_env_file():
    """Обновляет .env файл для использования OpenRouter"""
    
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
    backup_path = Path('.env.backup-fireworks')
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
    
    # Запрашиваем API ключ OpenRouter
    print("\n🔑 Введите API ключ OpenRouter")
    print("(Получить можно на https://openrouter.ai/keys)")
    openrouter_key = input("API Key (sk-or-v1-...): ").strip()
    
    if not openrouter_key or not openrouter_key.startswith('sk-or-'):
        print("❌ Неверный формат ключа. Ключ должен начинаться с 'sk-or-'")
        return False
    
    # Создаем новый .env
    new_env = f"""# Конфигурация обновлена скриптом configure_openrouter.py

# Telegram Bot Token
TELEGRAM_TOKEN={telegram_token or ''}

# OpenRouter Configuration
OPENAI_API_KEY={openrouter_key}
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Модели
MODEL=meta-llama/llama-3.2-3b-instruct:free
MODEL_QUERY_TRANSFORM=meta-llama/llama-3.2-3b-instruct:free
EMBEDDING_MODEL=openai/text-embedding-3-small

# RAGAS Evaluation модели
RAGAS_LLM_MODEL=meta-llama/llama-3.2-3b-instruct:free
RAGAS_EMBEDDING_MODEL=openai/text-embedding-3-small
RAGAS_EMBEDDING_PROVIDER=openai

# Embeddings Provider
EMBEDDING_PROVIDER=openai

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
    print("  LLM: meta-llama/llama-3.2-3b-instruct:free")
    print("  Embeddings: openai/text-embedding-3-small")
    print("\n⚠️  Примечание: Используются бесплатные модели с rate limits")
    print("  Рекомендуется использовать маленький датасет для evaluation")
    print("\n🚀 Запустите бота: make run")
    
    return True

def main():
    print("=" * 60)
    print("🔄 Переключение на OpenRouter")
    print("=" * 60)
    
    if update_env_file():
        print("\n✨ Готово!")
    else:
        print("\n❌ Не удалось обновить конфигурацию")

if __name__ == '__main__':
    main()

