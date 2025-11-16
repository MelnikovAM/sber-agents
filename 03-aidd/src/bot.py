import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_URL, HISTORY_LEN
from logger import setup_logging
import httpx

# Глобальное хранилище контекста пользователей
user_contexts = {}

async def start_handler(message: types.Message):
    welcome_text = (
        "👋 Привет! Я — твой персональный тренер по фитнесу.\n\n"
        "Задавай мне любые вопросы о тренировках, питании, упражнениях — "
        "и я помогу тебе достичь твоих фитнес-целей!\n\n"
        "📋 Доступные команды:\n"
        "/start — показать это сообщение\n"
        "/clear — очистить историю диалога\n\n"
        "Просто напиши свой вопрос, и я отвечу! 💪"
    )
    await message.answer(welcome_text)

async def clear_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_contexts:
        user_contexts[user_id] = []
    await message.answer("История диалога очищена.")

async def ask_llm(message_text: str, user_id: int) -> str:

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "aleksei-telegram-fitness-bot",
        "X-Title": "FitnessTelegramBot",
        "Content-Type": "application/json"
    }
    
    # Получаем историю пользователя
    history = user_contexts.get(user_id, [])
    
    # Формируем messages: system + история + новое сообщение
    messages = [
        {"role": "system", "content": "Ты — персональный тренер по фитнесу. Отвечай кратко, понятно и профессионально."}
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": message_text})
    
    json_data = {
        "model": OPENROUTER_MODEL,
        "messages": messages
    }
    try:
        print(f"Request URL: {OPENROUTER_URL}")
        print(f"Request model: {OPENROUTER_MODEL}")
        
        async with httpx.AsyncClient(follow_redirects=False) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=json_data, timeout=30)
            print(f"Response status: {resp.status_code}")
            print(f"Response headers: {dict(resp.headers)}")
            print(f"Response text (first 200 chars): {resp.text[:200]}")
            
            if resp.status_code != 200:
                print(f"Error response: {resp.text[:500]}")
                return "Извините, не удалось получить ответ. Попробуйте позже."
            
            content_type = resp.headers.get("content-type", "")
            if "application/json" not in content_type:
                print(f"Unexpected content-type: {content_type}")
                print(f"Full response: {resp.text[:1000]}")
                return "Извините, не удалось получить ответ. Попробуйте позже."
            
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    
    except httpx.HTTPStatusError as e:
        logging.error(f"LLM HTTP Status Error: {e.response.status_code}")
        print(f"Response text: {e.response.text[:500]}")
        return "Извините, не удалось получить ответ. Попробуйте позже."

    except Exception as e:
        logging.error(f"LLM Error: {e}")
        import traceback
        traceback.print_exc()
        return "Извините, не удалось получить ответ. Попробуйте позже."

    
async def llm_handler(message: types.Message):
    user_id = message.from_user.id
    
    try:
        reply = await ask_llm(message.text, user_id)
        
        # Сохраняем в историю: вопрос пользователя и ответ ассистента
        if user_id not in user_contexts:
            user_contexts[user_id] = []
        
        user_contexts[user_id].append({"role": "user", "content": message.text})
        user_contexts[user_id].append({"role": "assistant", "content": reply})
        
        # Обрезаем историю до последних N пар (user+assistant)
        max_messages = HISTORY_LEN * 2
        if len(user_contexts[user_id]) > max_messages:
            user_contexts[user_id] = user_contexts[user_id][-max_messages:]
        
    except Exception as e:
        logging.error(f"LLM Handler Error: {e}")
        reply = "Извините, не удалось получить ответ. Попробуйте позже."
    
    await message.answer(reply)

async def main():
    setup_logging()
    logging.info("Бот запускается...")
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(start_handler, Command(commands=["start"]))
    dp.message.register(clear_handler, Command(commands=["clear"]))
    dp.message.register(llm_handler)
    
    logging.info("Бот запущен и готов к работе (polling)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
