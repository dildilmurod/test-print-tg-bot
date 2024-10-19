from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_categories, get_product_by_category, get_category, get_product

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Продукты'), KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Настройки'), KeyboardButton(text='Помощь')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт...')

products = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Маски', callback_data='mask')],
    [InlineKeyboardButton(text='Умывалки', callback_data='washgel')],
    [InlineKeyboardButton(text='БАДы', callback_data='supplement')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Youtube', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')]
])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                                 resize_keyboard=True)
get_location = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить локацию', request_location=True)]],
                                   resize_keyboard=True)


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data="to_main"))
    return keyboard.adjust(2).as_markup()


async def products(category_id):
    all_products = await get_product_by_category(category_id)
    keyboard = InlineKeyboardBuilder()
    for product in all_products:
        keyboard.add(InlineKeyboardButton(text=product.name, callback_data=f"product_{product.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data="to_main"))
    return keyboard.adjust(2).as_markup()


to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='На главную', callback_data="to_main")]
])
