# -------------------------Первый бот (синхронный)------------------------- #


import telebot
import time
import psutil

bot = telebot.TeleBot("BOT_TOKEN")


@bot.message_handler(commands=['start'])
def start(message):
    start_time = time.time()
    bot.send_message(message.chat.id,
                     "Привет! Я синхронный бот. Отправь мне команду /slow для запуска длительной операции.")
    end_time = time.time()
    execution_time = end_time - start_time

    memory_usage = psutil.virtual_memory().used / (1024 * 1024)
    
    print(f"Функция start выполнена за {execution_time:.2f} секунд")
    print(f"Использование оперативной памяти: {memory_usage:.2f} MB")
    print("")


@bot.message_handler(commands=['slow'])
def slow_operation(message):
    start_time = time.time()
    bot.send_message(message.chat.id, "Начинаю выполнение длительной операции...")
    start_memory = psutil.virtual_memory().used
    time.sleep(5)
    bot.send_message(message.chat.id, "Длительная операция завершена.")
    end_time = time.time()
    execution_time = end_time - start_time

    end_memory = psutil.virtual_memory().used
    memory_usage = abs(end_memory - start_memory) / (1024 * 1024)

    print(f"Функция slow_operation выполнена за {execution_time:.2f} секунд")
    print(f"Использование оперативной памяти: {memory_usage:.2f} MB")

    performance = 5 / execution_time
    efficiency = execution_time / 5

    print(f"Время отклика: {execution_time:.2f} секунд")
    print(f"Производительность: {performance:.2f} сообщений в секунду")
    print(f"Эффективность использования ресурсов: {efficiency:.2f}")
    print("")


bot.polling(none_stop=True)


# -------------------------Первый бот (асинхронный)------------------------- #


import asyncio
import time
from aiogram import Bot, Dispatcher, types, executor
import psutil

bot = Bot(token="BOT_TOKEN")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_time = time.time()
    await message.answer("Привет! Я асинхронный бот. Отправь мне команду /slow для запуска длительной операции.")
    end_time = time.time()
    execution_time = end_time - start_time

    memory_usage = psutil.virtual_memory().used / (1024 * 1024)

    print(f"Функция start выполнена за {execution_time:.2f} секунд")
    print(f"Использование оперативной памяти: {memory_usage:.2f} MB")
    print("")


@dp.message_handler(commands=['slow'])
async def slow_operation(message: types.Message):
    start_time = time.time()
    await message.answer("Начинаю выполнение длительной операции...")
    start_memory = psutil.virtual_memory().used
    await asyncio.sleep(5)
    await message.answer("Длительная операция завершена.")

    end_time = time.time()
    execution_time = end_time - start_time

    end_memory = psutil.virtual_memory().used
    memory_usage = abs(end_memory - start_memory) / (1024 * 1024)

    print(f"Функция slow_operation выполнена за {execution_time:.2f} секунд")
    print(f"Использование оперативной памяти: {memory_usage:.2f} MB")

    performance = 5 / execution_time
    efficiency = execution_time / 5

    print(f"Время отклика: {execution_time:.2f} секунд")
    print(f"Производительность: {performance:.2f} сообщений в секунду")
    print(f"Эффективность использования ресурсов: {efficiency:.2f}")
    print("")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


# -------------------------Второй бот (синхронный)------------------------- #


import telebot
import requests
import time
import psutil

bot = telebot.TeleBot("BOT_TOKEN")


@bot.message_handler(commands=['start'])
def start(message):
    start_time = time.time()
    start_cpu_time = psutil.cpu_times()
    start_memory = psutil.virtual_memory().used

    n_requests = 30
    url = "https://www.hse.ru/"
    session = requests.Session()
    for i in range(n_requests):
        bot.send_message(message.chat.id, f"Making request to {url}")
        resp = session.get(url)
        if resp.status_code == 200:
            pass

    end_time = time.time()
    end_cpu_time = psutil.cpu_times()
    end_memory = psutil.virtual_memory().used

    execution_time = end_time - start_time
    user_time = end_cpu_time.user - start_cpu_time.user
    sys_time = end_cpu_time.system - start_cpu_time.system

    memory_usage = abs(end_memory - start_memory) / (1024 * 1024)

    print(f"Real time: {execution_time:.3f}s")
    print(f"User time: {user_time:.3f}s")
    print(f"Sys time: {sys_time:.3f}s")
    print(f"Memory usage: {memory_usage:.2f} MB")
    print("")


bot.polling(none_stop=True)


# -------------------------Второй бот (асинхронный)------------------------- #


import asyncio
import aiohttp
import psutil
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token="BOT_TOKEN")
dp = Dispatcher(bot)


async def make_request(session, req_n, chat_id):
    url = "https://www.hse.ru/"
    await bot.send_message(chat_id, f"Making request to {url}")
    async with session.get(url) as resp:
        if resp.status == 200:
            await resp.text()


async def main(chat_id):
    start_time = asyncio.get_event_loop().time()
    start_cpu_time = psutil.cpu_times()
    start_memory = psutil.virtual_memory().used

    n_requests = 30
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[make_request(session, i, chat_id) for i in range(n_requests)])

    end_time = asyncio.get_event_loop().time()
    end_cpu_time = psutil.cpu_times()
    end_memory = psutil.virtual_memory().used

    execution_time = end_time - start_time
    user_time = end_cpu_time.user - start_cpu_time.user
    sys_time = end_cpu_time.system - start_cpu_time.system

    memory_usage = abs(end_memory - start_memory) / (1024 * 1024)

    print(f"Real time: {execution_time:.3f}s")
    print(f"User time: {user_time:.3f}s")
    print(f"Sys time: {sys_time:.3f}s")
    print(f"Memory usage: {memory_usage:.2f} MB")
    print("")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await main(message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)








