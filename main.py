import logging
import crets
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import aiogram.utils.markdown as md
import pandas as pd
from binance.um_futures import UMFutures


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initializate bot and dispatcher
bot = Bot(token=crets.tg_key, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
client = UMFutures()

help_command = """
/help - command list
/exchanges - cryptocurrency exchanges list"""

# exchanges = """
# Binance
# Huobi
# OKX"""

kb = ReplyKeyboardMarkup(resize_keyboard=True)
butt_1 = KeyboardButton('/help')
butt_2 = KeyboardButton('/exchanges')

kb.add(butt_1,).add(butt_2,)

kb_exchanges = ReplyKeyboardMarkup(resize_keyboard=True)
butt_exchanges_1 = KeyboardButton('/Binance')
# butt_exchanges_2 = KeyboardButton('/Huobi')
# butt_exchanges_3 = KeyboardButton('/OKX')

kb_exchanges.add(butt_exchanges_1,)#.add(butt_exchanges_2, butt_exchanges_3)

async def on_startup(_):
    print('Bot is up! \nReady to use')


# Start command handler
@dp.message_handler(commands='start')
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=md.text('Hello! Welcome to <b>Crypto Cryptocurrency Statistic Bot</b>'),
                           reply_markup=kb)
    await message.delete()
    user_id = message.from_user.id
    print(user_id)
@dp.message_handler(commands='help')
async def help_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=help_command, reply_markup=kb)
    await message.delete()

@dp.message_handler(commands='exchanges')
async def exchanges_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=md.text('<b>Select Exchanges</b>'),
                           reply_markup=kb_exchanges)
    await message.delete()

@dp.message_handler(commands='Binance')
async def binance_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=f'Please write Coin name you want know price. \n'
                                                              f'Example: BTCUSDT',
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def user_msg_cmd(message: types.Message):
    user_msg = message.text
    def ticker():
        tiker = client.book_ticker()
        i = 0
        coin_list = []
        while i < len(tiker):
            coin_ticker = tiker[i]
            coin_list.append(coin_ticker["symbol"])
            i += 1
        return coin_list
    coin_list = ticker()

    if user_msg in coin_list:
        price = client.ticker_price(symbol=user_msg)
        await bot.send_message(chat_id=message.from_user.id, text=f'{user_msg} -> {price["price"]}$')
    else:
        await bot.send_message(chat_id=message.from_user.id, text=f"Not find this coin: {user_msg}")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
