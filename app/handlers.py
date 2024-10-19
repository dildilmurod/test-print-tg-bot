from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

from app.middlewares import TestMiddleware

router = Router()


# router.message.middleware(TestMiddleware())


class Reg(StatesGroup):
    location = State()
    phone = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply(
        'Добро пожаловать в бот HoloSkin. Вы находитесь в Главном меню. Пожалуйста выберите нужный раздел',
        reply_markup=kb.main)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply(f'Hey {message.from_user.id} \n {message.from_user.first_name}')


@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(
        photo='AgACAgIAAxkBAAMIZomHRYJD0fyYjjZmguWzdT1_ZK8AAvHhMRuwfUlIxiQoqyMYRD4BAAMCAAN5AAM1BA',
        caption="This is your photo")


@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'Photo ID: {message.photo[-1].file_id}')


@router.message(F.text == 'Продукты')
async def catalog(message: Message) -> object:
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.products(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('product_'))
async def category(callback: CallbackQuery):
    product_data = await rq.get_product(callback.data.split('_')[1])
    await callback.answer(f'Вы выбрали Товар')
    await callback.message.answer(f'{product_data.name} \n{product_data.description} \n{product_data.price}',
                                  reply_markup=kb.to_main)


@router.callback_query(F.data == 'to_main')
async def return_main(callback: CallbackQuery):
    await callback.message.answer(
        'Вы находитесь в Главном меню. Пожалуйста выберите нужный раздел',
        reply_markup=kb.main)


# @router.message(Command('contact'))
# async def cmd_contact(message: Message):
#     await message.answer('Отправьте номер телефона', reply_markup=kb.get_number)
#
#
# @router.message(F.contact)
# async def contact_rec(message: Message):
#     await message.answer(message.contact.phone_number)

@router.message(F.text == 'Настройки')
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.location)
    await message.answer('Отправьте локацию', reply_markup=kb.get_location)


@router.message(Reg.location, F.location)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(location=message.location)
    await state.set_state(Reg.phone)
    await message.answer('Отправьте номер телефона', reply_markup=kb.get_number)


@router.message(Reg.phone, F.contact)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Thank you\nName: {data["location"]}\nPhone: {data["phone"]}')
    await state.clear()
