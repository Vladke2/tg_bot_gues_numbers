from aiogram.utils import executor
from botss import dp
import commands


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
