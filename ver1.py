from aiogram import Dispatcher,F,types,Bot
from datetime import datetime
import asyncio
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,FSInputFile
import os
from aiogram.filters import CommandStart,Command
from dotenv import find_dotenv,load_dotenv
from pprint import pprint
import time

load_dotenv(find_dotenv())
target_group_id =os.getenv('GROUP')

bot = Bot(token = os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

markup_start = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Залишити замовлення 📦'),KeyboardButton(text='Отримати консультацію 👩‍💼')]
        ,]
    ,resize_keyboard=True)

dict_offer = {'date':'','number':'','name':'','mark':'','size':''}
marks = ['M100','M150','M200','M250','M300','M350','M400','M450','M500']

def marki(message: types.Message, dict_offer):
    dict_offer['mark'] = message.text
    return message.answer('Скільки кубів бетону вам потрібно ?', reply_markup=types.ReplyKeyboardRemove())

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f'Вас вітає бот компанії ЛОТОС 👋 \n'
                                          f'Тут ви можете отримати швидку консультацію 👩‍💼 \nАбо залишити замовлення 🚛')
    await message.answer('Оберіть послугу', reply_markup=markup_start)

@dp.message(F.text == '/menu')
async def menu(message: types.Message):
    await message.answer('Початкове меню', reply_markup=markup_start)

@dp.message(F.text == 'Отримати консультацію 👩‍💼')
async def echo(message: types.Message):
        markup_consul = ReplyKeyboardMarkup(keyboard=[
                                                       [KeyboardButton(text='PriceList🧾')],
                                                       [KeyboardButton(text='Як замовити бетон 📞')],
                                                       [KeyboardButton(text='Доставка🚛')],
                                                       [KeyboardButton(text='🔙 Повернутись назад')],
                                                       ],)
        await message.answer('З якого питання вам потрібна допомога ?', reply_markup=markup_consul)

@dp.message(F.text == 'PriceList🧾')
async def price(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(r'C:\Users\admin\PycharmProjects\lotosbot\.venv\img\pricelist.jpg'))

@dp.message(F.text == 'Як замовити бетон 📞')
async def tutorial_order(message: types.Message):
    await message.answer('Щоб замовити бетон вам потрібно зателефонувати за номером\n+380 721-45-45\n'
                                         'Або залишити замовлення прямо в боті,для цього вам потрібно повернутися в головне меню)\n'
                                         '\nПісля замовлення наш менеджер звяжеться з вами) ')

@dp.message(F.text == 'Доставка🚛')
async def delivery(message: types.Message):
    await message.answer('Доставка може бути здійсненна протягом 24 годин,або на будь який потрібний вам час)')

@dp.message(F.text == 'Залишити замовлення 📦')
async def order(message: types.Message):

    markup_order = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='M100'),KeyboardButton(text='M150')],
                                         [KeyboardButton(text='M200'),KeyboardButton(text='M250')],
                                         [KeyboardButton(text='M300'),KeyboardButton(text='M350')],
                                         [KeyboardButton(text='M400'),KeyboardButton(text='M450')],
                                         [KeyboardButton(text='M500')],],resize_keyboard=True)

    await message.answer('Оберіть марку бетону', reply_markup=markup_order)

@dp.message(F.text == '🔙 Повернутись назад')
async def back(message: types.Message):
    await message.answer('Початкове меню',reply_markup=markup_start)

@dp.message(F.text =='✅ Підтвердити замовлення ✅')
async def finish(message: types.Message):
    global dict_offer, target_group_id
    dict_offer['date'] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    dict_offer['name'] = message.chat.first_name
    await message.answer('Дякую за замовлення ! \nНаш менеджер скоро звяжеться з вами 👩‍💼',reply_markup=types.ReplyKeyboardRemove())

    with open('data.txt', 'a', encoding='utf-8') as fl:
        fl.write('\n')
        pprint(dict_offer, stream=fl)
    await bot.send_message(chat_id = target_group_id, text=f'{str(dict_offer)}')

@dp.message(F.text)
async def num(message: types.Message):
    global dict_offer,marks
    if message.text in marks:
        dict_offer['mark'] = message.text
        await message.answer('Скільки кубів бетону вам потрібно ?', reply_markup=types.ReplyKeyboardRemove())
    else:
        for i in message.text:

            if i.isalpha():
                await message.answer('Неправильний формат відповіді', reply_markup=markup_start)
                break
            else:
                dict_offer['size'] = message.text
                markup_num = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text='Надати номер телефону', request_contact=True)],
                              ])
                await message.answer('Надайте ваш контакт ⬇️', reply_markup=markup_num)
                break

@dp.message(F.content_type == 'contact')
async def handle_contact(message):
    global dict_offer
    contact = message.contact
    dict_offer['number'] = contact.phone_number
    markup_acess = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='✅ Підтвердити замовлення ✅')]])
    await message.answer('Підтвердіть замовлення ⬇️', reply_markup=markup_acess)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())