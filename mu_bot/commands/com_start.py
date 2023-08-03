import random
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from botss import dp, bot


class RN(StatesGroup):
    random_number = State()
    number = State()
    maximum = State()


messages_store = {}


def get_messages(message: types.Message):
    index = 0
    if message.from_user.is_bot:
        index = message.chat.id
    else:
        index = message.from_user.id
    messages = messages_store.get(index)
    if messages:
        messages.add(message.message_id)
    else:
        messages_store.update({index: { message.message_id, } })
        messages = messages_store.get(index)
    return messages


@dp.message_handler(commands=["clear"])
async def clear(message: types.Message):
    messages = messages_store.get(message.from_user.id)
    if not messages:
        return
    for mess in messages:
        await bot.delete_message(message_id=mess, chat_id=message.chat.id)
    messages.clear()
    await message.reply("(🇺🇦)Історія очищена\
                        \n(🇬🇧)History is cleared")


@dp.message_handler(commands=('cancel'), state='*')
async def cancel_operation(message: types.Message, state: FSMContext):
    messages = get_messages(message)
    await state.finish()
    message = await message.answer('(🇺🇦)Гру скасована\nЩоб грати знову натисніть /start.\
                        \n(🇬🇧)Game canceled\nTo play again press /start.')
    messages = get_messages(message)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    messages = get_messages(message)
    message = await message.answer(f"(🇺🇦)Привіт {message.from_user.first_name}👋!\
    \nВибери максимальне значення випадкового числа 🎲\
    \n(🇬🇧)Hello {message.from_user.first_name}👋!\
    \nChoose the maximum value of the random number 🎲")
    await RN.random_number.set()
    messages = get_messages(message)


@dp.message_handler(lambda message: message.text.isdigit(), state=RN.random_number,)
async def random_number(message: types.Message, state: FSMContext):
    messages = get_messages(message)
    async with state.proxy() as data:
        data['maximum'] = int(message.text)
        data['random_number'] = random.randint(1, data['maximum'])
    await RN.next()
    message = await message.answer(f"(🇺🇦)Зрозуміло.максимальне значення випадкового числа {data['maximum']}\nГра почалась\
    \n(🇬🇧)Sure.maximum value of random number {data['maximum']}\nThe game has started")
    messages = get_messages(message)


@dp.message_handler(lambda message: message.text.isdigit(), state=RN.number)
async def answer(message: types.Message, state: FSMContext):
    messages = get_messages(message)
    async with state.proxy() as data1:
        if int(message.text) > data1['maximum']:
            message = await message.answer('(🇺🇦)максимальне число меньше ⤵\n(🇬🇧)the maximum number is less ⤵')
        else:
            if int(message.text) == data1['random_number']:
                message = await message.answer('(🇺🇦)🎉 Вітаю ти вгадав 🎉!\nНатисни /start щоб грати знову 🥇\
                            \n(🇬🇧)🎉 Congratulations, you guessed it 🎉!\nPress /start to play again 🥇')
                await state.finish()
            elif int(message.text) < data1['random_number']:
                message = await message.answer('(🇺🇦)Моє число більше👆👆\n(🇬🇧)My number is more👆👆')
            else:
                message = await message.answer('(🇺🇦)Моє число менше👇👇\n(🇬🇧)My number is less 👇👇')
    messages = get_messages(message)


@dp.message_handler(lambda message: non_isdigit, state=RN.number)
async def non_isdigit(message: types.Message):
    messages = get_messages(message)
    message = await message.answer('(🇺🇦)Введіть ціле число(1⃣)\n(🇬🇧)Enter an integer(1⃣')
    messages = get_messages(message)


@dp.message_handler(content_types=["text"], state='*')
async def text(message: types.Message):
    messages = get_messages(message)
    message = await message.answer('(🇺🇦)Введіть команду❗\n(🇬🇧)Enter the command❗')
    messages = get_messages(message)


@dp.message_handler(content_types=["photo", "sticker", "video", "animation",
                    'audio', 'document', 'voice'], state='*')
async def psva(message: types.Message):
    messages = get_messages(message)
    message = await message.answer('(🇺🇦)Навіщо це мені❓\n(🇬🇧)Why do I need this❓')
    messages = get_messages(message)
