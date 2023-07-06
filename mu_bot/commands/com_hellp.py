from aiogram import types
from mu_bot.botss import dp, bot
print(bot)


@dp.message_handler(commands=['hellp'])
async def hellp_info(message):
    button = types.InlineKeyboardMarkup(
        inline_keyboard=[
        [types.InlineKeyboardButton('Розпочати', callback_data='starts')],
    ])
    await message.reply("Hellow!\nI'm guess_the_number_Bot!\nPowered by aiogram.\nCreated by Vlad\n/start",
                        reply_markup=button)


@dp.callback_query_handler(lambda callb: callb.data == "starts")
async def execute_random(callb: types.CallbackQuery):
    await callb.answer('/start')
    await callb.message.reply('Натискай сюди щоб розпочати\n/start')