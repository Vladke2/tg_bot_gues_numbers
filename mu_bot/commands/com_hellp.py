from aiogram import types
from botss import dp, bot


@dp.message_handler(commands=['hellp','help'])
async def hellp_info(message):
    gif = 'bv0j-help'
    await bot.send_animation(gif)
    url = 'https://github.com/Vladke2'
    bot_data = await bot.get_me()
    button = types.InlineKeyboardMarkup(
        inline_keyboard=[
        [types.InlineKeyboardButton('Розпочати', callback_data='starts')],
            [types.InlineKeyboardButton('список команд', callback_data='list_of_commands')]
    ])
    await message.reply(f"Hellow!\nI'm {bot_data.first_name}!\nPowered by aiogram.\
    \nCreated by Vlad({url})",
                        reply_markup=button)


@dp.callback_query_handler(lambda callb: callb.data == "starts")
async def execute_random(callb: types.CallbackQuery):
    await callb.answer('/start')
    await callb.message.answer('(🇺🇦)Натискай сюди щоб розпочати\n/start \
                              \n(🇬🇧)Click here to start\n/start')

@dp.callback_query_handler(lambda callb: callb.data == "list_of_commands")
async def execute_random(callb: types.CallbackQuery):
    await callb.answer('/start,/clear,/cancel,/hellp,/help')
    await callb.message.reply('/start\n/clear\n/cancel\n/hellp,/help')
