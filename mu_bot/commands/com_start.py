import random
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from mu_bot.botss import dp, bot
print(bot)


class RN(StatesGroup):
    random_number = State()
    number = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт👋!\nВибрери максимальне значення випадкового числа 🎲")
    await RN.random_number.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=RN.random_number,)
async def random_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        maximum = int(message.text)
        data['random_number'] = random.randint(1, maximum)
    await RN.next()
    await message.reply(f"Зрозуміло.максимальне значеннн випадкового числа {maximum}\nГра почалась")


@dp.message_handler(lambda message: message.text.isdigit(), state=RN.number)
async def answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data1:
        if int(message.text) == data1['random_number']:
            await message.reply('🎉 Ввітаю ти вгадав 🎉!\nНатисни /start щоб грати знову 🥇')
            await state.finish()
        elif int(message.text) < data1['random_number']:
            await message.reply('Ні\nМоє число більше👆👆')
        else:
            await message.reply('Ні\nМоє число менше👇👇')
