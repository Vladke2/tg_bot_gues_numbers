from aiogram.utils import executor
from mu_bot.botss import dp, bot
from mu_bot.commands import com_hellp
from mu_bot.commands import com_start
print(bot)
print(com_hellp)
print(com_start)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
