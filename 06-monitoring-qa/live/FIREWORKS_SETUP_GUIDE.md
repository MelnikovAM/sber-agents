# Исправление ошибки trust_remote_code

## 🔴 Текущая проблема

```
ValueError: Please pass the argument `trust_remote_code=True` to allow custom code to be run.
```

Модель `nomic-ai/nomic-embed-text-v1.5` требует разрешения на запуск кастомного кода.

## ✅ Исправлено в коде

Обновлены файлы:
- ✅ `src/indexer.py` - добавлен `trust_remote_code=True`
- ✅ `src/evaluation.py` - добавлен `trust_remote_code=True`

## 🚀 Два варианта настройки Fireworks

### Вариант 1: Fireworks API + HuggingFace Embeddings (локально) ⭐ Рекомендуется

**Преимущества:**
- ✅ Бесплатные embeddings (работают локально)
- ✅ Качественная модель nomic-ai
- ✅ Не тратите кредиты на embeddings

**Откройте `.env` и установите:**

```bash
# Fireworks AI для LLM
OPENAI_API_KEY=fw_XXXXXXXXXXXXXXXX
OPENAI_BASE_URL=https://api.fireworks.ai/inference/v1

# LLM модели (через Fireworks API)
MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
MODEL_QUERY_TRANSFORM=accounts/fireworks/models/llama-v3p3-70b-instruct
RAGAS_LLM_MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct

# Embeddings (локально через HuggingFace)
EMBEDDING_PROVIDER=huggingface
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5

# RAGAS Embeddings (локально через HuggingFace)
RAGAS_EMBEDDING_PROVIDER=huggingface
RAGAS_EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
```

### Вариант 2: Полностью через Fireworks API

**Преимущества:**
- ✅ Проще настроить
- ✅ Все в одном месте

**Недостатки:**
- ⚠️ Тратятся кредиты на embeddings
- ⚠️ Нужно проверить поддержку модели embeddings

**Откройте `.env` и установите:**

```bash
# Fireworks AI
OPENAI_API_KEY=fw_XXXXXXXXXXXXXXXX
OPENAI_BASE_URL=https://api.fireworks.ai/inference/v1

# Все модели через Fireworks API
MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
MODEL_QUERY_TRANSFORM=accounts/fireworks/models/llama-v3p3-70b-instruct
RAGAS_LLM_MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct

# Embeddings через Fireworks API (проверьте поддержку!)
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
RAGAS_EMBEDDING_PROVIDER=openai
RAGAS_EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
```

**ВНИМАНИЕ:** Если Fireworks не поддерживает `nomic-ai/nomic-embed-text-v1.5`, используйте Вариант 1.

## 📝 Проверка работы

После обновления `.env`:

### 1. Перезапустите бота

```bash
# Остановите текущий процесс (Ctrl+C)
make run
```

### 2. Проверьте индексацию

В Telegram отправьте:
```
/index
```

Должна пройти успешно без ошибок.

### 3. Проверьте статус

```
/index_status
```

Должно показать ~589 документов.

### 4. Задайте тестовый вопрос

```
Какие условия по вкладам?
```

Должен получить ответ на основе документов.

## 🐛 Если все еще есть ошибки

### Проблема: Модель все еще требует trust_remote_code

**Решение:** Перезапустите бота после изменений в `.env`

### Проблема: Fireworks не поддерживает embedding модель

**Решение:** Используйте Вариант 1 (HuggingFace локально)

### Проблема: Долго загружается модель embeddings

**Решение:** Это нормально при первом запуске - модель скачивается (~ 500 MB)

## 💡 Рекомендация

**Используйте Вариант 1** - это даст вам:
- Быстрые и качественные embeddings без затрат
- Стабильную работу
- Экономию кредитов Fireworks

Единственный минус - первый запуск займет 1-2 минуты для скачивания модели.

