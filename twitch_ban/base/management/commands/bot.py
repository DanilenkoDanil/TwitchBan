import os
import django
import logging
from aiogram import Bot, Dispatcher, executor, types
from django.core.management.base import BaseCommand
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from base.models import Chanel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

logging.basicConfig(level=logging.INFO)

first_button = InlineKeyboardButton("Список каналов", callback_data="list")
second_button = InlineKeyboardButton("Добавить канал", callback_data="add")
keyboard = InlineKeyboardMarkup().add(first_button, second_button)

bot = Bot(token="5826015068:AAGmVwCYBxSthSqAIEUbIhxCrWEgw5RkjqE")

dp = Dispatcher(bot, storage=MemoryStorage())
flags = {'ge': '🇩🇪'}


class TableState(StatesGroup):
    title = State()
    url = State()
    viewers = State()
    country = State()
    notes = State()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ["list"])
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    for channel in Chanel.objects.all():
        delete_button = InlineKeyboardButton("Удалить канал", callback_data=f"delete_{channel.id}")
        msg_keyboard = InlineKeyboardMarkup().add(delete_button)
        if channel.ban_date:
            message = f"{channel.id} {channel.title} - 🇩🇪\n👀 {channel.spectators} ❤️ {channel.subscribers}\n{channel.link}\n❌ - {channel.ban_date}\nДобавлен - {channel.add_date}\n---------------------\n{channel.notes}"
        else:
            message = f"{channel.id} {channel.title} - 🇩🇪\n👀 {channel.spectators} ❤️ {channel.subscribers}\n{channel.link}\n✅ - Активен\nДобавлен - {channel.add_date}\n---------------------\n{channel.notes}"
        user_id = callback_query.from_user.id
        await bot.send_message(user_id, message, disable_web_page_preview=True, reply_markup=msg_keyboard)


@dp.callback_query_handler(lambda c: "delete" in c.data)
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    channel_id = int(str(callback_query.data).split('_')[1])
    Chanel.objects.get(id=channel_id).delete()
    await callback_query.message.answer('Удален!', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ["add"])
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Введите название канала...')
    await TableState.title.set()


@dp.message_handler(state=TableState.title)
async def process_title(message, state):
    await state.update_data(title=message.text)
    await message.answer('Введите ссылку...')
    await TableState.url.set()


@dp.message_handler(state=TableState.url)
async def process_url(message, state):
    await state.update_data(url=message.text)
    await message.answer('Введите страну...')
    await TableState.country.set()


@dp.message_handler(state=TableState.country)
async def process_url(message, state):
    await state.update_data(country=message.text)
    await message.answer('Введите заметку...')
    await TableState.notes.set()


@dp.message_handler(state=TableState.notes)
async def process_country(message, state):
    await state.update_data(notes=message.text)
    data = await state.get_data()
    Chanel.objects.create(title=data['title'], link=data['url'], county=data['country'], notes=data['notes'])
    await bot.send_message(chat_id=message.chat.id, text='Добавлено', reply_markup=keyboard)
    await state.finish()


class Command(BaseCommand):
    help = 'Старт ТГ-бота'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)
