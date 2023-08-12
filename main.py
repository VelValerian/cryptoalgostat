import logging
import crets
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import aiogram.utils.markdown as md

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initializate bot and dispatcher
bot = Bot(token=crets.tg_key, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

help_command = """
/help - command list
/exchanges - cryptocurrency exchanges list"""

kb = ReplyKeyboardMarkup(resize_keyboard=True)
butt_1 = KeyboardButton('/help')
butt_2 = KeyboardButton('/exchanges')

kb.add(butt_1,).add(butt_2,)

async def on_startup(_):
    print('Bot is up! \nReady to use')

# Start command handler
@dp.message_handler(commands='help')
async def help_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=help_command, reply_markup=kb)

@dp.message_handler(commands='exchanges')
async def country_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=, reply_markup=kb)
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)