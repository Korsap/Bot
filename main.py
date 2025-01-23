import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from router import *

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

log(START)

async def main():
    dp.include_router(router)  # Подключаем маршруты
    try:
        await dp.start_polling(bot)  # Запускаем бота
    except Exception as e:
        log(f"Ошибка: {e}. Перезапуск через 15 секунд...")
        await asyncio.sleep(15)
        await main()    

if __name__ == '__main__':
    asyncio.run(main())
