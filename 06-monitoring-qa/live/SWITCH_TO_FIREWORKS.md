# Переключение на Fireworks AI

## Шаг 1: Получите API ключ Fireworks

1. Зарегистрируйтесь на https://fireworks.ai/
2. Перейдите в https://fireworks.ai/api-keys
3. Создайте новый API ключ (начинается с `fw_`)

## Шаг 2: Обновите .env файл

Откройте `.env` и измените следующие строки:

```bash
# Fireworks AI Configuration
OPENAI_API_KEY=fw_XXXXXXXXXXXXXXXX
OPENAI_BASE_URL=https://api.fireworks.ai/inference/v1

# Модели (актуальные на 2024)
MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
MODEL_QUERY_TRANSFORM=accounts/fireworks/models/llama-v3p3-70b-instruct
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5

# RAGAS Evaluation модели
RAGAS_LLM_MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
RAGAS_EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
RAGAS_EMBEDDING_PROVIDER=openai
```

## Шаг 3: Перезапустите бота

```bash
make run
```

## Преимущества Fireworks AI

✅ Более высокие rate limits
✅ Более стабильный API
✅ Быстрые модели (llama-v3p3-70b-instruct)
✅ Хорошие embeddings (nomic-ai/nomic-embed-text-v1.5)

## Альтернативные модели Fireworks

Если llama-v3p3-70b-instruct недоступна, попробуйте:

```bash
# Более легкая модель
MODEL=accounts/fireworks/models/llama-v3p1-8b-instruct

# Или Qwen
MODEL=accounts/fireworks/models/qwen2p5-72b-instruct
```

## Проверка работы

После перезапуска бота проверьте:

```
/index_status  # Проверить индексацию
```

Затем задайте тестовый вопрос:

```
Какие условия по вкладам?
```

Если получили ответ - всё работает! ✅

