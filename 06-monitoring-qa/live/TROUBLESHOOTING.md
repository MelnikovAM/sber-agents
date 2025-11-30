# Устранение ошибок бота

## 🔴 Текущая проблема: 401 Authentication Error

### Симптомы

```
AuthenticationError: Error code: 401 - {'error': {'message': 'No cookie auth credentials found', 'code': 401}}
```

- ❌ Большинство RAGAS метрик возвращают `nan`
- ✅ Только `answer_similarity` и `context_precision` частично работают
- ❌ Evaluation не может завершиться успешно

### Причина

API ключ OpenRouter недействителен, истек или не установлен правильно.

### Решение

#### Вариант 1: Обновить ключ OpenRouter

1. Перейдите на https://openrouter.ai/keys
2. Создайте новый API ключ
3. Откройте `.env` и обновите:
   ```bash
   OPENAI_API_KEY=sk-or-v1-XXXXXXXXXXXXXXXX
   ```

#### Вариант 2: Переключиться на Fireworks AI ⭐ (Рекомендуется)

**Быстрый способ:**

```bash
# 1. Запустите скрипт настройки
python3 configure_fireworks.py

# 2. Перезапустите бота
make run
```

**Ручной способ:**

1. Получите API ключ на https://fireworks.ai/api-keys
2. Откройте `.env` и измените:

```bash
OPENAI_API_KEY=fw_XXXXXXXXXXXXXXXX
OPENAI_BASE_URL=https://api.fireworks.ai/inference/v1
MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
MODEL_QUERY_TRANSFORM=accounts/fireworks/models/llama-v3p3-70b-instruct
EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
RAGAS_LLM_MODEL=accounts/fireworks/models/llama-v3p3-70b-instruct
RAGAS_EMBEDDING_MODEL=nomic-ai/nomic-embed-text-v1.5
```

3. Перезапустите бота:
   ```bash
   make run
   ```

## ✅ Проверка работы

После исправления проверьте:

### 1. Индексация
```
/index_status
```

Должно показать количество проиндексированных документов.

### 2. Простой вопрос
```
Какие условия по вкладам?
```

Должен получить ответ на основе документов.

### 3. Evaluation (если нужно)
```
/evaluate_dataset 06-rag-qa-small
```

Должны получить результаты метрик без ошибок.

## 📊 Другие возможные проблемы

### Rate Limits (429 ошибка)

**Симптомы:**
```
429 Too Many Requests
```

**Решение:**
1. Подождите 15-20 минут
2. Используйте маленький датасет: `/evaluate_dataset 06-rag-qa-small`
3. Уменьшите количество метрик в `src/evaluation.py`

### Connection Error (APIConnectionError)

**Симптомы:**
```
APIConnectionError: Connection error
```

**Решение:**
1. Проверьте интернет-соединение
2. Проверьте, что `OPENAI_BASE_URL` корректен
3. Попробуйте другой провайдер

### Numpy not available

**Симптомы:**
```
RuntimeError: Numpy is not available
```

**Решение:**
```bash
# Уже исправлено в pyproject.toml
# Если возникает снова:
uv sync
```

### Missing einops package

**Симптомы:**
```
ImportError: This modeling file requires the following packages that were not found in your environment: einops
```

**Решение:**
```bash
# Уже добавлено в pyproject.toml
uv sync
# Затем перезапустите бота
make run
```

### trust_remote_code Error

**Симптомы:**
```
ValueError: Please pass the argument `trust_remote_code=True` to allow custom code to be run
```

**Решение:**
```bash
# Уже исправлено в src/indexer.py и src/evaluation.py
# Просто перезапустите бота
make run
```

## 📝 Логи

Логи бота находятся в:
```
logs/bot.log
```

Просмотр последних ошибок:
```bash
tail -50 logs/bot.log | grep ERROR
```

## 🆘 Если ничего не помогает

1. Удалите виртуальное окружение и пересоздайте:
   ```bash
   rm -rf .venv
   uv sync
   ```

2. Проверьте все переменные в `.env`:
   ```bash
   cat .env
   ```

3. Создайте новый `.env` из примера:
   ```bash
   cp env.example .env
   # Отредактируйте .env
   ```

4. Проверьте версии пакетов:
   ```bash
   uv run python -c "import torch; import numpy; print(f'torch: {torch.__version__}'); print(f'numpy: {numpy.__version__}')"
   ```

## 💡 Контакты поддержки

- Fireworks AI: https://fireworks.ai/support
- OpenRouter: https://openrouter.ai/docs
- LangSmith: https://smith.langchain.com/support

