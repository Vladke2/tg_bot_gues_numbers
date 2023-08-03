import random
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from botss import dp
import time


class RNv(StatesGroup):
    number_m = State()
    number_b = State()


@dp.message_handler(commands=['start_versa','startversa'])
async def send_welcome(message: types.Message):
    await message.answer(f"(🇺🇦)Привіт {message.from_user.first_name}👋!\
        \nЗагадай число від 1 до 10 та напиши його мені 🗯\
        \n(🇬🇧)Hello {message.from_user.first_name}👋!\
        \n Name a number from 1 to 10 and write it to me 🗯")
    await RNv.number_m.set()



@dp.message_handler(lambda message: message.text.isdigit(), state=RNv.number_m)
async def number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_m'] = int(message.text)
        if data['number_m'] < 1:
            await message.answer('(🇺🇦)Загадай число більше 0❗⬆\n(🇬🇧)Guess the number greater than 0❗⬆')
        elif data['number_m'] >= 10:
            await message.answer('(🇺🇦)Загадай число меньше 10❗⬇\n(🇬🇧)Name a number less than 10❗⬇')
        else:
            await message.answer(f"(🇺🇦)Зрозуміло.Число яке ви загадали {data['number_m']}\
                            \n(🇬🇧)It's clear. The number you guessed {data['number_m']}")
    await message.answer(f'(🇺🇦)Ти хочеш змінити число❓\n(🇬🇧)Do you want to change the number❓')
    await RNv.next()


@dp.message_handler(lambda message: non_isdigit, state=RNv.number_m)
async def non_isdigit(message: types.Message):
    message = await message.answer('(🇺🇦)Введіть ціле число(1⃣)\n(🇬🇧)Enter an integer(1⃣')


@dp.message_handler(content_types='text', state=RNv.number_b)
async def answer(message: types.Message, state: FSMContext):
    number_b = random.randint(1, 10)
    sleep = [0.25, 0.5, 0.75]
    if message.text == 'ні':
        time.sleep(sleep[random.randint(1, 2)])
        await message.answer(f'(🇺🇦)Це число {number_b}❓(🇬🇧)Is this number {number_b}❓')
    elif message.text == 'так':
        await message.answer('(🇺🇦)Ура! Дякую що зіграв зі мною\nХочеш ще❓Якщо так то натискай сюди ➡ /start_versa ⬅\
        (🇬🇧)Cheers! Thanks for playing with me\nWant more❓ If so, click here ➡ /start_versa ⬅')
        await state.finish()
