import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_URL
import httpx

async def start_handler(message: types.Message):
    await message.answer("Привет! Я фитнес-бот. Задай любой вопрос, и я помогу тебе как персональный тренер.")

async def ask_llm(message_text: str) -> str:

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "aleksei-telegram-fitness-bot",
        "X-Title": "FitnessTelegramBot",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Ты — персональный тренер по фитнесу. Отвечай кратко, понятно и профессионально."},
            {"role": "user", "content": message_text}
        ]
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
        print(f"LLM HTTP Status Error: {e.response.status_code}")
        print(f"Response text: {e.response.text[:500]}")
        return "Извините, не удалось получить ответ. Попробуйте позже."

    except Exception as e:
        print(f"LLM Error: {e}")
        import traceback
        traceback.print_exc()
        return "Извините, не удалось получить ответ. Попробуйте позже."

    
async def llm_handler(message: types.Message):
    try:
        reply = await ask_llm(message.text)
    except Exception as e:
        print("LLM Error:", e)
        reply = "Извините, не удалось получить ответ. Попробуйте позже."
    await message.answer(reply)

async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(start_handler, Command(commands=["start"]))
    dp.message.register(llm_handler)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
