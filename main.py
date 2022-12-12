import aiogram
import sqlite3
import math
import random
from random import randint
import logging
import time
from asyncio import sleep
from matplotlib.pyplot import box
import timedelta
import datetime
from time import gmtime, strftime
from time import localtime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import os, re, configparser, requests
from aiogram.types import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import quote_html
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.filters import Text
from gtts import gTTS
import config
import users
import chats
from telegram_bot_pagination import InlineKeyboardPaginator
from alive import keep_alive

bot = aiogram.Bot(config.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


#Стата
@dp.message_handler(commands=['юзеры', 'статистика', 'stats', 'users'],
                    commands_prefix='!./')
async def statistic(message: types.Message):
    us = users.cursor.execute("SELECT * FROM users").fetchall()
    ch = chats.cursor.execute("SELECT * FROM chats").fetchall()
    await message.answer(f'<b>USERS: {len(us)}</b>\n<b>GROUPS: {len(ch)}</b>')


#Пинг
@dp.message_handler(commands=['ping', 'пинг'], commands_prefix=["/", "!"])
async def ping(message: types.Message):
    a = time.time()
    bot_msg = await message.answer(f'Проверяю пинг...')
    if bot_msg:
        b = time.time()
        await bot_msg.edit_text(f'Пинг бота: {round((b-a)*1000)} мс.')


#botadmins_cmd
@dp.message_handler(commands=['botadmins'])
async def botadmins_cmd(message: types.Message):
    await message.reply(f'{config.botadmins}')


#start_cmd
@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    await message.reply(f"""Приветствую дорогой пользователь бота SUNRISE 🌄
Данный бот создан исключительно в развлекательных целях, удачного пользования!
👥📢 Оффтоп чат - @sunrise_offtop
👨‍💻📢 Чат тех. поддержки - @sunrise_help_chat
🔎💬 Официальный канал -
🗒️✅ Сайт (сайт бота) -

👨‍💻✅ Администраторы бота: /botadmins

🔎 Список команд вы можете узнать написав:
/cmd_rp - список рп команд 💬;
/cmd_basic - основные команды бота 🗒️;
/cmd_admins - команды для модераторов чата 👤;
/cmd_games - список игровых команд 🎮.
""")


@dp.message_handler(commands=['cmd_games'])
async def cmd_games(message):
    await message.reply(f"""🎮 Список игровых команд бота:
<code>Дартс - (ставка) Игра в дартс 🎯
Фут - (ставка) Игра в футбол ⚽
Баскет - (ставка) Игра в баскетбол 🏀
Боул - (ставка) Игра в боулинг 🎳
Казино - (ставка) Игра в казино 🎰
Куб - [1-6] (ставка) Игра в кости 🎲
Камень/️Ножницы/Бумага - (ставка) 🗿✂📃
+Леденец или /led - растить свой леденец, каждые 3 часа 🍭</code>""",
                        parse_mode="html")


@dp.message_handler(commands="cmd_admins")
async def cmd_admins(message: types.Message):
    if message.chat.type == "private":
        await message.reply(f"❗️<b>ЭТИ КОМАНДЫ ПРЕДНАЗНАЧЕНЫ ДЛЯ ЧАТОВ</b>❗️",
                            parse_mode="html")
    else:
        await message.reply(f"""
❗️<b>КОМАНДЫ ДОЛЖНЫ БЫТЬ ОТВЕТОМ НА СООБЩЕНИЕ</b>❗️
Список команд для Администраторов:
<code>/mute - заткнуть пользователя
/ban - забанить пользователя
/del - удалить сообщение</code>

Противоположные команды:
<code>/unmute - размут
/unban - разбан</code>

❗️<b>СЛЕДУЩИЕ КОМАНДЫ УЖЕ НЕ ДОЛЖНЫ БЫТЬ ОТВЕТОМ НА СООБЩЕНИЕ</b>❗️
<code>/staff - список всех модераторов канала</code>""",
                            parse_mode="html")


character_pages = [
    """👥💬 Рп команды бота:
<code>Брак</code> - реплай на той(-м), с кем хотите вступить в брак 💍
<code>Развод</code> - расторгнуть брак со своей парой 💔
<code>Мой брак</code> - посмотреть свой брак 👰♥️🤵
<code>Передать</code> (сумма) - передать указанное кол-во монет 💰
<code>Ключи</code> - с ним можно открыть кейс 🔑
<code>Купить</code> портфель «1-3» «кол-ство» портфелей» - очевидно
<code>Открыть</code> портфель «1-3» - "даже не знаю"
<code>/promo</code> (Промокод) - ввод промокода для получения вознаграждения 📃
<code>Поцеловать</code> - поцелуй
<code>Банкай</code> - применить банкай
<code>Расенган</code> - ёбнуть расенганом
<code>Гетсуга</code> - использовать гетсугу
<code>Чмок</code> - чмокнуть
<code>Чпок</code> - чпокнуть
<code>Тык</code> - доебаться или тыкнуть
<code>Пнуть</code> - мистер очевидность
<code>Лизнуть</code> - мистер очевидность
<code>Отсосать</code> - мистер очевидность
<code>!пинг</code> - пинг бота""", """👥💬 Рп команды бота:
<code>+ | ++ | +++</code> - добавить респект пользователю
<code>Конфеты</code> - приобрести конфеты
<code>Отлизать</code> - мистер очевидность
<code>Отдаться</code> - мистер очевидность
<code>Раздеть</code> - мистер очевидность
<code>Обнять</code> - мистер очевидность
<code>Выебать</code> - мистер очевидность
<code>Трахнуть</code> - мистер очевидность
<code>Отхуярить</code> - мистер очевидность
<code>Заебашить</code> - мистер очевидность
<code>Кусь</code> - кусьнуть
<code>Продать</code> - мистер очевидность"""
]


@dp.message_handler(commands=['cmd_rp'])
async def cmd_rp(message, page=1):

    paginator = InlineKeyboardPaginator(len(character_pages),
                                        current_page=page,
                                        data_pattern='character#{page}')

    await bot.send_message(message.chat.id,
                           character_pages[page - 1],
                           reply_markup=paginator.markup,
                           parse_mode='html')


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'character')
async def cmd_rp_call(call):
    page = int(call.data.split('#')[1])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await cmd_rp(call.message, page)


@dp.message_handler(commands=['cmd_basic'])
async def cmd_basic(message):
    await message.reply(f"""🗒️ Основные команды бота:
/start - начать пользоваться ботом ✅
/help - дополнительная информация о боте 📃
/rp - кастомная рп команда (только для участников с VIP статусом) 💎
/name  - введите, чтобы указать новый ник 📝
/q - вопрос администрации 👨‍💻
/bio - установить описание профиля (только для участников с VIP статусом) 💎
/rules - установить правила чата 📝
/chatinfo - установить описание чата (только для чатов с VIP статусом) 💎
Баланс - баланс
/bind - привязать чат
/unbind - отвязать чат
/use - использовать увелечитель
""",
                        parse_mode="Markdown")


#start_cmd
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    # status = "Пользователь"
    # bio = "Не установлено!"
    # chat = "Не привязан!"
    # promo = "Нет"
    # vip = "Отсутствует!"
    now = datetime.datetime.now()
    regdata = now.strftime("%a, %d %b %Y")
    led_time = now.strftime('%H:%M:%S')
    chatid = message.chat.id
    chatname = message.chat.title
    chatusername = message.chat.username
    chatbio = "Отсутствует!"
    chatrules = "Не установлены!"
    vipchat = "Отсутствует!"
    chatregdata = now.strftime("%a, %d %b %Y")
    users.cursor.execute(f"SELECT id FROM users WHERE id = '{id}'")
    if message.chat.type == 'supergroup':
        if users.cursor.fetchone() is None:
            users.cursor.execute(
                "INSERT INTO users (id, name, username, regdata, led_time) VALUES (?, ?, ?, ?, ?);",
                (id, name, username, regdata, led_time))
            users.connect.commit()
            await message.reply(
                f'Привет {name}! Вы успешно зарегистрировались в боте, узнайте подробную информацию введя /help'
            )
            await bot.send_message(
                -5695410762,
                f'📊 Новый пользователь!\nID: <code>{id}</code>\nНик: {name}\nЮзернейм: @{username}\nРегистрация произошла в чате: @{chatusername}'
            )
        else:
            await message.reply(f'✅ Вы уже зарегистрированы!')
        chats.cursor.execute(
            f"SELECT chatid FROM chats WHERE chatid = '{chatid}'")
        if chats.cursor.fetchone() is None:
            chats.cursor.execute(
                "INSERT INTO chats VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
                (chatid, chatname, chatusername, chatbio, chatrules, 0,
                 vipchat, chatregdata))
            chats.connect.commit()
            await message.answer(f'✅ Чат успешно зарегистрирован!')
            await bot.send_message(
                -5695410762,
                f'📊 Новый чат!\nCHAT_ID: <code>{chatid}</code>\nНазвание: {chatname}\nСсылка: {chatusername}'
            )
        else:
            pass
    elif message.chat.type == 'private':
        if users.cursor.fetchone() is None:
            users.cursor.execute(
                "INSERT INTO users (id, name, username, regdata, led_time) VALUES (?, ?, ?, ?, ?);",
                (id, name, username, regdata, led_time))
            users.connect.commit()
            await message.reply(
                f'Привет {name}! Вы успешно зарегистрировались в боте, узнайте подробную информацию введя /help'
            )
            await bot.send_message(
                -5695410762,
                f'📊 Новый пользователь!\nID: <code>{id}</code>\nНик: {name}\nЮзернейм: @{username}'
            )
        else:
            await message.reply(f'✅ Вы уже зарегистрированы!')


#Инвентарь
@dp.message_handler(commands=['инв', 'инвентарь', 'inv', 'склад'],
                    commands_prefix='!./')
async def invent(message: types.Message):
    id = message.from_user.id
    balance = users.cursor.execute("SELECT balance from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    balance = (balance[0])
    coins = users.cursor.execute("SELECT coins from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    coins = (coins[0])
    medal1 = users.cursor.execute("SELECT medal1 from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    medal1 = (medal1[0])
    medal2 = users.cursor.execute("SELECT medal2 from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    medal2 = (medal2[0])
    medal3 = users.cursor.execute("SELECT medal3 from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    medal3 = (medal3[0])
    keys = users.cursor.execute("SELECT keys from users where id = ?",
                                (message.from_user.id, )).fetchone()
    keys = (keys[0])
    boxes1 = users.cursor.execute("SELECT boxes1 from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    boxes1 = (boxes1[0])
    boxes2 = users.cursor.execute("SELECT boxes2 from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    boxes2 = (boxes2[0])
    boxes3 = users.cursor.execute("SELECT boxes3 from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    boxes3 = (boxes3[0])
    candy = users.cursor.execute("SELECT candy from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    candy = (candy[0])
    await message.reply(f"""📔 Ваш инвентарь:
<code>Баланс: {balance} 💰
Донат: {coins} 💳
Ключи: {keys} 🔑
Конфет: {candy} 🍬
Ящик I уровня: {boxes1} 💼
Ящик II уровня: {boxes2} 📦
Ящик III уровня: {boxes3} 🎁
Медалей за 1 место: {medal1} 🥇
Медалей за 2 место: {medal2} 🥈
Медалей за 3 место: {medal3} 🥉
</code>""",
                        parse_mode="html")


#Профиль
#Профиль
@dp.message_handler(commands=['инфа', 'инф', 'инфо', 'info', 'стата'],
                    commands_prefix='!./')
async def information(message: types.Message):
    id = message.from_user.id
    name = users.cursor.execute("SELECT name from users where id = ?",
                                (message.from_user.id, )).fetchone()
    name = (name[0])
    username = users.cursor.execute("SELECT username from users where id = ?",
                                    (message.from_user.id, )).fetchone()
    username = (username[0])
    balance = users.cursor.execute("SELECT balance from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    balance = (balance[0])
    coins = users.cursor.execute("SELECT coins from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    coins = (coins[0])
    led = users.cursor.execute("SELECT led from users where id = ?",
                               (message.from_user.id, )).fetchone()
    led = (led[0])
    status = users.cursor.execute("SELECT status from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    status = (status[0])
    regdata = users.cursor.execute("SELECT regdata from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    regdata = (regdata[0])
    marry = users.cursor.execute("SELECT marry from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    marry = (marry[0])
    marry_time = users.cursor.execute(
        "SELECT marry_time FROM users WHERE id = ?",
        (message.from_user.id, )).fetchone()
    marry_time = (marry_time[0])
    res = users.cursor.execute("SELECT respect from users where id = ?",
                               (message.from_user.id, )).fetchone()
    res = (res[0])
    vip = users.cursor.execute("SELECT vip from users where id = ?",
                               (message.from_user.id, )).fetchone()
    vip = (vip[0])
    wins = users.cursor.execute("SELECT wins from users where id = ?",
                                (message.from_user.id, )).fetchone()
    wins = (wins[0])
    loses = users.cursor.execute("SELECT loses from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    loses = (loses[0])
    games = users.cursor.execute("SELECT games from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    games = (games[0])
    chat = users.cursor.execute("SELECT chat from users where id = ?",
                                (message.from_user.id, )).fetchone()
    chat = (chat[0])
    words = users.cursor.execute("SELECT words from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    words = (words[0])

    profile_info = f"""• Никнейм: {name} 🏷️
• Юзернейм: {username} 
• Баланс: {balance} 💰
• Донат: {coins} 💳
• Уважение: {res} 📈
• Статус: {status} 👤
• Сообщений написано: {words} 💬
• Размер леденца: {led} 🍭
• VIP статус: {vip} ⚖️🤑
• Всего игр: {games} 🎰
• Проигрышей | Побед: {loses} 👎 | {wins} 🏆
• Зарегистрирован: {regdata} 📃"""

    if str(chat) == 'Не привязан!':
        if games != 0:
            procent = int(wins) / int(games)
            prcnt = float(procent) * 100
            if marry == 0:
                profile_info += f"\n• Процент побед: {prcnt}%"
                await message.reply(f"{profile_info}")
            else:
                marred = await bot.get_chat(marry)
                mname = quote_html(marred.full_name)
                # mname = "Пёс"
                profile_info += f"\n• Процент побед: {prcnt}%"
                profile_info += f"\n• Вы в браке с {mname} ❤️ \n• Время брака: {marry_time}"
                await message.reply(f"{profile_info}")
        else:
            if marry == 0:
                await message.reply(f"{profile_info}")
            else:
                marred = await bot.get_chat(marry)
                mname = quote_html(marred.full_name)
                # mname = "Пёс"
                profile_info += f"\n• Вы в браке с {mname} ❤️ \n• Время брака: {marry_time}"

                await message.reply(f"{profile_info}")
    else:
        if games != 0:
            procent = int(wins) / int(games)
            prcnt = float(procent) * 100
            if marry == 0:
                profile_info += f"\n• Процент побед: {prcnt}%"
                profile_info += f"\n• Гражданин чата: <code>{chat}</code>"
                await message.reply(f"{profile_info}")
            else:
                marred = await bot.get_chat(marry)
                mname = quote_html(marred.full_name)
                # mname = "Пёс"
                profile_info += f"\n• Процент побед: {prcnt}%"
                profile_info += f"\n• Вы в браке с {mname} ❤️ \n• Время брака: {marry_time} \n• Гражданин чата: <code>{chat}</code>"
                await message.reply(f"{profile_info}")
        else:
            if marry == 0:
                profile_info += f"\n• Гражданин чата: <code>{chat}</code>"
                await message.reply(f"{profile_info}")
            else:
                marred = await bot.get_chat(marry)
                mname = quote_html(marred.full_name)
                # mname = "Пёс"
                profile_info += f"\n• Вы в браке с {mname} ❤️ \n• Время брака: {marry_time} \n• Гражданин чата: <code>{chat}</code>"
                await message.reply(f"{profile_info}")


#keys
@dp.message_handler(regexp=r"(^Конфеты|конфеты) ?(\d+)?")
async def buy_keys(message: types.Message):
    command_parse = re.compile(r"(^Конфеты|конфеты) ?(\d+)?")
    parsed = command_parse.match(message.text)
    suma = parsed.group(2)
    summ = 1500000 * int(suma)
    msg = message
    id = msg['from']['id']
    data = {}
    data["summ"] = summ
    data['user_id'] = message.from_user.id
    data1 = {}
    data1["suma"] = suma
    data1['user_id'] = message.from_user.id
    name = message.from_user.get_mention(as_html=True)
    balance = users.cursor.execute("SELECT balance from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    balance = (balance[0])
    candy = users.cursor.execute("SELECT candy from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    candy = (candy[0])
    if int(balance) >= summ:
        users.cursor.execute(
            """UPDATE users SET balance = balance - :summ WHERE id = :user_id;""",
            data)
        users.cursor.execute(
            """UPDATE users SET candy = candy + :suma WHERE id = :user_id;""",
            data1)
        users.connect.commit()
        await message.reply(
            f'Вы успешно приобрели {suma} 🍬\nПотрачено: <code>{summ}</code> 💰')
        await bot.send_message(
            -5695410762,
            f'<code>Пользователь {name}, ID: {id}\nПриобрёл: {suma} 🍬\nНа сумму: {summ} 💰</code>'
        )
    else:
        await message.reply(
            f'Для покупки нужно <code>{summ}</code> 💰, а у вас <code>{balance}</code> 💰'
        )


@dp.message_handler(commands=['use', 'увеличить', 'увеличитель'],
                    commands_prefix='!./')
async def use(message):
    msg = message
    id = msg['from']['id']
    name = message.from_user.get_mention(as_html=True)
    led = users.cursor.execute("SELECT led from users where id = ?",
                               (message.from_user.id, )).fetchone()
    led = (led[0])
    candy = users.cursor.execute("SELECT candy from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    candy = (candy[0])
    if int(candy) >= 1:
        users.cursor.execute(
            f'UPDATE users SET candy = {candy - 1}  WHERE id=?',
            (message.from_user.id, ))
        users.cursor.execute(f'UPDATE users SET led = {led + 20} WHERE id=?',
                             (message.from_user.id, ))
        users.connect.commit()
        await message.answer(
            f'{name}, вы успешно использовали конфету-увеличитель, ваш леденец вырос на 20 см.\nтеперь его длина - {led + 20} см.\nКонфет-увеличителей - {candy - 1} 🍬'
        )
    else:
        await message.reply(f'У тебя нет конфеты-увеличителя!')


#Открыть портфель
@dp.message_handler(lambda message: message.text.lower().startswith(
    ('открыть портфель ', 'Открыть портфель ')))
async def open_box(message: types.Message):
    bugg = message.text.lower().split()[2]
    try:
        if int(bugg) >= 1 and int(bugg) <= 3:
            boxes = users.cursor.execute(
                f"SELECT boxes{str(bugg)} from users where id = ?",
                (message.from_user.id, )).fetchone()
            boxes = (boxes[0])
            keys = users.cursor.execute("SELECT keys from users where id = ?",
                                        (message.from_user.id, )).fetchone()
            keys = (keys[0])
            if int(boxes) >= 1:
                if int(keys) >= 1:
                    btn = types.InlineKeyboardButton(
                        'Открыть! ✅', callback_data=f'open_box_{bugg}')
                    kb = types.InlineKeyboardMarkup().add(btn)
                    await message.reply("Нажмите чтобы открыть портфель.",
                                        reply_markup=kb)
                else:
                    await message.reply(
                        f'У вас нет ключа для открытия портфеля ⛔')
            else:
                await message.reply(f'У вас нет портфеля для открытия ⛔')
    except:
        pass


@dp.callback_query_handler(lambda c: c.data.startswith('open_box_'))
async def open_box_query(c: types.CallbackQuery):
    id = c.data.split('_')[2]
    boxes = users.cursor.execute(
        f"SELECT boxes{id} from users where id = ?",
        (c.message.reply_to_message.from_user.id, )).fetchone()
    boxes = (boxes[0])
    if int(boxes) >= 1:
        print(boxes)
        await bot.answer_callback_query(c.id)
        if int(id) == 1:
            money = randint(10000, 25000)
            candyes = randint(1, 2)
            keyes = randint(1, 3)
        elif int(id) == 2:
            money = randint(50000, 100000)
            candyes = randint(4, 6)
            keyes = randint(3, 5)
        elif int(id) == 3:
            money = randint(150000, 200000)
            candyes = randint(10, 13)
            keyes = randint(5, 8)

        win = ['money', 'candy', 'keys']
        w = random.choice(win)

        if str(w) == 'money':
            await c.message.answer(
                f'Вы успешно открыли портфель <code>«{id}»</code> и получили <code>{money}</code> 💰',
                parse_mode="html")
            users.cursor.execute(
                f'UPDATE users SET balance = balance + {money} WHERE id=?',
                (c.message.reply_to_message.from_user.id, ))
        elif str(w) == 'candy':
            await c.message.answer(
                f'Вы успешно открыли портфель <code>«{id}»</code> и получили <code>{candyes}</code> 🍬',
                parse_mode="html")
            users.cursor.execute(
                f'UPDATE users SET candy = candy + {candyes} WHERE id=?',
                (c.message.reply_to_message.from_user.id, ))
        elif str(w) == 'keys':
            await c.message.answer(
                f'Вы успешно открыли портфель <code>«{id}»</code> и получили <code>{keyes}</code> 🔑',
                parse_mode="html")
            users.cursor.execute(
                f'UPDATE users SET keys = keys + {keyes} WHERE id=?',
                (c.message.reply_to_message.from_user.id, ))

        users.cursor.execute(f"UPDATE users SET keys = keys - 1 WHERE id = ?",
                             (c.message.reply_to_message.from_user.id, ))
        users.cursor.execute(
            f'UPDATE users SET boxes{id} = boxes{id} - 1 WHERE id=?',
            (c.message.reply_to_message.from_user.id, ))
        users.connect.commit()

        await bot.delete_message(c.message.chat.id, c.message.message_id)
    else:
        await c.message.reply(f'У вас нет портфеля для открытия ⛔')


#Био
@dp.message_handler(commands=['bio'])
async def setbio(message: types.Message):
    args = message.get_args()
    name1 = message.from_user.get_mention(as_html=True)
    users.cursor.execute("SELECT bio FROM users WHERE id=?",
                         (message.from_user.id, ))
    data = users.cursor.fetchone()
    vip = users.cursor.execute("SELECT vip from users where id = ?",
                               (message.from_user.id, )).fetchone()
    vip = (vip[0])
    if str(vip) == 'Активен':
        if len(args) <= 100:
            if args:
                if data is None:
                    return await message.reply("Не найден в базе данных!")
                users.cursor.execute(f'UPDATE users SET bio=? WHERE id=?', (
                    args,
                    message.from_user.id,
                ))
                users.connect.commit()
                await message.reply(f"Описание {name1}, изменено!")
            else:
                await message.reply('Ваше описание не может быть пустым!')
        else:
            await message.reply(
                'Максимальная длина био должна составлять 100 символов!')
    else:
        await message.reply(
            f'Данная команда доступна лишь пользователям с VIP статусом 💎')


#Правила
@dp.message_handler(lambda message: message.text.lower() == 'био')
async def bio_text(message: types.Message):
    bio = users.cursor.execute("SELECT bio from users where id = ?",
                               (message.from_user.id, )).fetchone()
    bio = (bio[0])
    await message.reply(f'✅📃 Ваше описание профиля:\n{bio}')


#Своя рп
@dp.message_handler(commands=['rp'])
async def custom_rp(message: types.Message):
    args = message.get_args()
    reply = message.reply_to_message
    vip = users.cursor.execute("SELECT vip from users where id = ?",
                               (message.from_user.id, )).fetchone()
    vip = (vip[0])
    if str(vip) == 'Активен':
        if reply:
            name1 = message.from_user.get_mention(as_html=True)
            name2 = message.reply_to_message.from_user.get_mention(
                as_html=True)
            await message.answer(f'{name1}\n{args}\n{name2}')
        else:
            name1 = message.from_user.get_mention(as_html=True)
            await message.answer(f'{name1} {args}')
    else:
        await message.reply(
            f'Данная команда доступна лишь пользователям с VIP статусом 💎')


#Ник
@dp.message_handler(commands=['name'])
async def setname(message: types.Message):
    args = message.get_args()
    name1 = message.from_user.get_mention(as_html=True)
    users.cursor.execute("SELECT name FROM users WHERE id=?",
                         (message.from_user.id, ))
    data = users.cursor.fetchone()
    if len(args) <= 10:
        if args:
            if data is None:
                return await message.reply("Не найден в базе данных!")
            users.cursor.execute(f'UPDATE users SET name=? WHERE id=?', (
                args,
                message.from_user.id,
            ))
            users.connect.commit()
            await message.reply(f"Ник {name1}, изменён на «{args}»")
        else:
            await message.reply('Ник не может быть пустым!')
    else:
        await message.reply(
            'Максимальная длина ника должна составлять 10 символов!')


#Гражданство
@dp.message_handler(
    commands=['привязать', 'bind', 'чат', 'chat', 'гражданство'],
    commands_prefix='+!./')
async def bind(message: types.Message):
    chat = users.cursor.execute("SELECT chat from users where id = ?",
                                (message.from_user.id, )).fetchone()
    chat = (chat[0])
    chatname = message.chat.title
    await message.reply(f'Чат успешно привязан ✅')
    users.cursor.execute(f'UPDATE users SET chat=? WHERE id=?', (
        chatname,
        message.from_user.id,
    ))
    users.connect.commit()


@dp.message_handler(commands=['отвязать', 'unbind'], commands_prefix='+!./')
async def bind(message: types.Message):
    await message.reply(f'Чат успешно отвязан ✅')
    users.cursor.execute(f'UPDATE users SET chat=? WHERE id=?', (
        'Не привязан!',
        message.from_user.id,
    ))
    users.connect.commit()


#Правила
@dp.message_handler(lambda message: message.text.lower() == 'правила')
async def rules_text(message: types.Message):
    rules = chats.cursor.execute(
        "SELECT chatrules from chats where chatid = ?",
        (message.chat.id, )).fetchone()
    rules = (rules[0])
    await message.answer(f'🗒️ Правила чата {message.chat.title}:\n{rules}')


#Правила чата
@dp.message_handler(commands=['rules'])
async def cmd_rules(message: types.Message):
    args = message.get_args()
    chatid = message.chat.id
    if not args:
        await message.answer("Введите правила!")
    else:
        rules = chats.cursor.execute(
            "SELECT chatrules from chats where chatid = ?",
            (message.chat.id, )).fetchone()
        rules = (rules[0])
        chats.cursor.execute(f'UPDATE chats SET chatrules=? WHERE chatid=?', (
            args,
            message.chat.id,
        ))
        chats.connect.commit()
        await message.answer('Правила чата изменены! 🗒️')


#Просмотр описания чата
@dp.message_handler(lambda message: message.text.lower() == 'описание чата')
async def chatbio_text(message: types.Message):
    bio = chats.cursor.execute("SELECT chatbio from chats where chatid = ?",
                               (message.chat.id, )).fetchone()
    bio = (bio[0])
    vip = chats.cursor.execute("SELECT vipchat from users where chatid = ?",
                               (message.chat.id, )).fetchone()
    vip = (vip[0])
    if str(vip) == 'Активен':
        await message.answer(f'Описание чата:\n{bio}')
    else:
        await message.reply(
            f'Данная команда доступна лишь чатам с VIP статусом 💎')


#Описание чата
@dp.message_handler(commands=['chatinfo'])
async def cmd_chat_bio(message: types.Message):
    args = message.get_args()
    chatid = message.chat.id
    vip = chats.cursor.execute("SELECT vipchat from chats where chatid = ?",
                               (message.chat.id, )).fetchone()
    vip = (vip[0])
    if str(vip) == 'Активен':
        if not args:
            await message.answer(f'Введите описание!')
        else:
            rules = chats.cursor.execute(
                "SELECT chatbio from chats where chatid = ?",
                (message.chat.id, )).fetchone()
            rules = (rules[0])
            chats.cursor.execute(f'UPDATE chats SET chatbii=? WHERE chatid=?',
                                 (
                                     args,
                                     message.chat.id,
                                 ))
            chats.connect.commit()
            await message.answer('Описание чата изменено! 🗒️')
    else:
        await message.reply(
            f'Данная команда доступна лишь чатам с VIP статусом 💎')


#Передачи
@dp.message_handler(regexp=r"(^Передать|передать) ?(\d+)?")
async def send_money(message: types.Message):
    balance = users.cursor.execute("SELECT balance from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    balance = (balance[0])
    command_parse = re.compile(r"(^Передать|передать) ?(\d+)?")
    parsed = command_parse.match(message.text)
    suma = parsed.group(2)
    name1 = message.reply_to_message.from_user.get_mention(as_html=True)
    name2 = message.from_user.get_mention(as_html=True)
    suma = int(suma)
    data = {}
    data["suma"] = suma
    data['user_id'] = message.reply_to_message.from_user.id
    data1 = {}
    data1["suma"] = suma
    data1['user_id'] = message.from_user.id
    if int(balance) >= suma:
        users.cursor.execute(
            """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
            data)
        users.cursor.execute(
            """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
            data1)
        await message.reply(
            f"{name2} отдал(а) {name1} - <code>{suma}</code> 💰",
            parse_mode='html')
    else:
        await message.reply(f"У вас недостаточно монет для передачи!",
                            parse_mode='html')
        users.connect.commit()


#Вопрос администрации
class Quest(StatesGroup):
    msg = State()


@dp.message_handler(commands=['обращение', 'q', 'вопрос'],
                    commands_prefix='!/')
async def question(message: types.Message):
    id = message.from_user.id
    await message.answer(
        '🖋 Введите текст/фото для обращения к администраторам бота :)')
    await Quest.msg.set()


@dp.message_handler(content_types=ContentType.ANY, state=Quest.msg)
async def quest_msgl(message: types.Message, state: FSMContext):
    await state.finish()
    i = '-1001392898291'
    name = message.from_user.get_mention(as_html=True)
    bot_msg = await message.answer(f'Обращение отправляется...')
    await bot.send_message(
        -1001392898291,
        f'Получено обращение!\n\nОтправитель: {name}\nID: {message.from_user.id}\nЮзернейм: @{message.from_user.username}\n\nОбращение:'
    )
    await message.copy_to(i)
    await bot_msg.edit_text(f'📣 Обращение отправлено!')


@dp.message_handler(lambda msg: msg.text.lower() == 'бот ливни')
async def bot_leave(message):
    stts = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    status = (stts[0])
    if str(status) == 'Создатель бота':
        await message.answer("3")
        await sleep(1)
        await message.answer("2")
        await sleep(1)
        await message.answer("1")
        await sleep(1)
        await message.answer("Goodbye my friends")
        await message.chat.leave()
    elif str(status) == 'Администратор':
        await message.answer("3")
        await sleep(1)
        await message.answer("2")
        await sleep(1)
        await message.answer("1")
        await sleep(1)
        await message.answer("Goodbye my friends")
        await message.chat.leave()
    else:
        await message.reply('Сам ливни, шакал')


#Игры
@dp.message_handler(regexp=r"(^Казино|казино) ?(\d+)?")
async def kazino(message: types.Message):
    msg = message
    stts = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    status = (stts[0])
    name = message.from_user.get_mention(as_html=True)
    command_parse = re.compile(r"(^Казино|казино) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    summ2 = int(summ)
    data = {}
    data["suma"] = int(summ)
    data['user_id'] = message.from_user.id
    data1 = {}
    data1["suma"] = (summ2)
    data1['user_id'] = message.from_user.id
    chance = randint(0, 100)
    balance = users.cursor.execute("SELECT balance from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    balance = (balance[0])
    if str(status) == 'Спонсор бота':
        if int(summ) <= 10000000000:
            if int(balance) >= int(summ):
                if int(chance) <= 49:
                    await message.answer(
                        f'{name}, ты проиграл(а) <code>{summ}</code>💰',
                        parse_mode='html')
                    users.cursor.execute(
                        """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                        data)
                    users.cursor.execute(
                        f'UPDATE users SET loses = loses + 1 WHERE id=?',
                        (message.from_user.id, ))
                    users.cursor.execute(
                        f'UPDATE users SET games = games + 1 WHERE id=?',
                        (message.from_user.id, ))
                elif int(chance) >= 50:
                    await message.answer(
                        f'{name}, ты выиграл(а) <code>{summ2}</code>💰',
                        parse_mode='html')
                    users.cursor.execute(
                        """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                        data1)
                    users.cursor.execute(
                        f'UPDATE users SET games = games + 1 WHERE id=?',
                        (message.from_user.id, ))
                    users.cursor.execute(
                        f'UPDATE users SET wins = wins + 1 WHERE id=?',
                        (message.from_user.id, ))
                    users.connect.commit()
            elif int(balance) < int(summ):
                await message.reply(
                    f'У тебя нет столько монет, твой баланс: <code>{balance}</code>💰 ',
                    parse_mode='html')
        else:
            await message.reply(
                f'Нельзя играть на суммы более <code>10000000000</code>💰',
                parse_mode='html')
    else:
        if int(summ) <= 1000000000:
            if int(balance) >= int(summ):
                if int(chance) <= 49:
                    await message.answer(
                        f'{name}, ты проиграл(а) <code>{summ}</code>💰',
                        parse_mode='html')
                    users.cursor.execute(
                        """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                        data)
                    users.cursor.execute(
                        f'UPDATE users SET loses = loses + 1 WHERE id=?',
                        (message.from_user.id, ))
                    users.cursor.execute(
                        f'UPDATE users SET games = games + 1 WHERE id=?',
                        (message.from_user.id, ))
                elif int(chance) >= 50:
                    await message.answer(
                        f'{name}, ты выиграл(а) <code>{summ2}</code>💰',
                        parse_mode='html')
                    users.cursor.execute(
                        """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                        data1)
                    users.cursor.execute(
                        f'UPDATE users SET wins = wins + 1 WHERE id=?',
                        (message.from_user.id, ))
                    users.cursor.execute(
                        f'UPDATE users SET games = games + 1 WHERE id=?',
                        (message.from_user.id, ))
                    users.connect.commit()
            elif int(balance) < int(summ):
                await message.reply(
                    f'У тебя нет столько монет, твой баланс: <code>{balance}</code>💰 ',
                    parse_mode='html')
        else:
            await message.reply(
                f'Нельзя играть на суммы более <code>1000000000</code>💰',
                parse_mode='html')


@dp.message_handler(regexp=r"(^Куб|куб) ?(\d+)? ?(\d+)?")
async def kub(message: types.Message):
    command_parse = re.compile(r"(^Куб|куб) ?(\d+)? ?(\d+)?")
    parsed = command_parse.match(message.text)
    dice_value = parsed.group(2)
    dice_value = int(dice_value)
    summ = parsed.group(3)
    summ = (summ)
    name1 = message.from_user.get_mention(as_html=True)
    if int(summ) <= int(1000000000):
        if dice_value > 6:
            await message.reply(
                f"Введите сообщение в формате: \n<b>Куб (число от 1 до 6) (ставка)</b>",
                parse_mode='html')
        else:
            if not summ:
                await message.reply(
                    f"Введите сообщение в формате: \n<b>Куб (число от 1 до 6) (ставка)</b>",
                    parse_mode='html')
            else:
                if not dice_value:
                    await message.reply(
                        f"Введите сообщение в формате:\n<b>Куб (число от 1 до 6) (ставка)</b>",
                        parse_mode='html')
                else:
                    balanc = users.cursor.execute(
                        "SELECT balance from users where id = ?",
                        (message.from_user.id, )).fetchone()
                    balance = (balanc[0])
                    summ = int(summ)
                    if balance >= summ:
                        dice_value = int(dice_value)
                        bot_data = await bot.send_dice(message.chat.id)
                        bot_data = bot_data['dice']['value']
                        plus = bot_data + 1
                        minus = bot_data - 1
                        summ2 = summ * 10
                        data = {}
                        data["suma"] = summ
                        data['user_id'] = message.from_user.id
                        data1 = {}
                        data1["suma"] = summ2
                        data1['user_id'] = message.from_user.id
                        await sleep(5)

                        if bot_data > dice_value:
                            await message.reply(
                                f'Ты проиграл(а) <b>{summ}</b>💰',
                                parse_mode='html')
                            users.cursor.execute(
                                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                                data)
                            users.cursor.execute(
                                f'UPDATE users SET games = games + 1 WHERE id=?',
                                (message.from_user.id, ))
                            users.cursor.execute(
                                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                                (message.from_user.id, ))

                        elif bot_data < dice_value:
                            await message.reply(
                                f'Ты проиграл(а) <b>{summ}</b>💰',
                                parse_mode='html')
                            users.cursor.execute(
                                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                                data)
                            users.cursor.execute(
                                f'UPDATE users SET games = games + 1 WHERE id=?',
                                (message.from_user.id, ))
                            users.cursor.execute(
                                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                                (message.from_user.id, ))
                        else:
                            await message.reply(
                                f'Ты выиграл(а) <b>{summ2}</b>💰',
                                parse_mode='html')
                            users.cursor.execute(
                                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                                data1)
                            users.cursor.execute(
                                f'UPDATE users SET games = games + 1 WHERE id=?',
                                (message.from_user.id, ))
                            users.cursor.execute(
                                f'UPDATE users SET wins = wins + 1 WHERE id=?',
                                (message.from_user.id, ))
                            users.connect.commit()
                    elif balance < summ:
                        balanc = users.cursor.execute(
                            "SELECT balance from users where id = ?",
                            (message.from_user.id, )).fetchone()
                        balance = (balanc[0])
                        await message.reply(
                            f'У тебя нет столько монет, твой баланс: <code>{balance}</code>💰 ',
                            parse_mode='html')
    else:
        await message.reply(
            f'Нельзя играть на сумы более <code>1000000000</code>💰',
            parse_mode='html')


@dp.message_handler(regexp=r"(камень|Камень) ?(\d+)?")
async def kamen(message: types.Message):
    command_parse = re.compile(r"(камень|Камень) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    summ = int(summ)
    name1 = message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = int(summ)
    data['user_id'] = message.from_user.id
    balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    balance = (balanc[0])
    if balance >= summ:
        rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумагу"])
        await message.answer("Я выбрал " + rand + "\nА ты выбрал 🗿Камень")
        if rand == '🗿Камень':
            await message.answer("Ничья⚔️")
        elif rand == '✂️Ножницы':
            await message.answer(f"Ты выиграл {summ}💰")
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET wins = wins + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        else:
            await message.answer(f"Я победил\nТы проиграл {summ}💰")
            users.cursor.execute(
                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
    elif balance < summ:
        await message.answer(
            f'{name1} у тебя нет столько 💰\nТвой баланс:<code>{balance}</code>💰 ',
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(regexp=r"(ножницы|Ножницы) ?(\d+)?")
async def nozhnicy(message: types.Message):
    command_parse = re.compile(r"(ножницы|Ножницы) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    summ = int(summ)
    name1 = message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = int(summ)
    data['user_id'] = message.from_user.id
    balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    balance = (balanc[0])
    if balance >= summ:
        rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумагу"])
        await message.answer("Я выбрал " + rand + "\nА ты выбрал ✂️Ножницы")
        if rand == '🗿Камень':
            await message.answer(f"Я победил\nТы проиграл {summ}💰")
            users.cursor.execute(
                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        elif rand == '✂️Ножницы':
            await message.answer("Ничья⚔️")
        else:
            await message.answer(f"Ты выиграл {summ}💰")
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET wins = wins + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
    elif balance < summ:
        await message.answer(
            f'{name1} у тебя нет столько 💰\nТвой баланс:<code>{balance}</code>💰 ',
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(regexp=r"(бумага|Бумага) ?(\d+)?")
async def bumaga(message: types.Message):
    command_parse = re.compile(r"(бумага|Бумага) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    summ = int(summ)
    name1 = message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = int(summ)
    data['user_id'] = message.from_user.id
    balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    balance = (balanc[0])
    if balance >= summ:
        rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумагу"])
        await message.answer("Я выбрал " + rand + "\nА ты выбрал 📄Бумагу")
        if rand == '🗿Камень':
            await message.answer(f"Ты выиграл {summ}💰")
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET wins = wins + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        elif rand == '✂️Ножницы':
            await message.answer(f"Я победил\nТы проиграл {summ}💰")
            users.cursor.execute(
                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        else:
            await message.answer("Ничья⚔️")
    elif balance < summ:
        await message.answer(
            f'{name1} у тебя нет столько 💰\nТвой баланс:<code>{balance}</code>💰 ',
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(regexp=r"(^Дартс|дартс) ?(\d+)?")
async def darts(message: types.Message):
    command_parse = re.compile(r"(^Дартс|дартс) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    name1 = message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = summ
    data['user_id'] = message.from_user.id
    balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    balance = (balanc[0])
    summ = int(summ)
    if balance >= summ:
        bot_data = await bot.send_dice(message.chat.id, emoji='🎯')
        bot_data = bot_data['dice']['value']
        await sleep(3)
        if bot_data == 6:
            await message.answer(
                f'{name1} ты попал(а) прямо в цель, и выиграл(а) - {summ}💰',
                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET games = wins + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        elif bot_data == 1:
            await message.answer(
                f'{name1} ты промазал(а) и проиграл(а) - {summ}💰',
                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        else:
            await message.reply(f'Такой себе бросок, деньги остаются при тебе')
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
    elif balance < summ:
        await message.answer(
            f'{name1} у тебя нет столько 💰\nТвой баланс:<code>{balance}</code>💰 ',
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(regexp=r"(^Боул|боул) ?(\d+)?")
async def boul(message: types.Message):
    command_parse = re.compile(r"(^Боул|боул) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    name1 = message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = summ
    data['user_id'] = message.from_user.id
    balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    balance = (balanc[0])
    summ = int(summ)
    if balance >= summ:
        bot_data = await bot.send_dice(message.chat.id, emoji='🎳')
        bot_data = bot_data['dice']['value']
        await sleep(3)
        if bot_data == 6:
            await message.answer(
                f'{name1} ты сбил(а) все кегли и выиграл(а) - {summ}💰',
                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET wins = wins + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        elif bot_data == 1:
            await message.answer(
                f'{name1} ты промазал(а) и проиграл(а) - {summ}💰',
                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        else:
            await message.anwer(
                f'{name1} такой себе бросок, деньги остаются при тебе')
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
    elif balance < summ:
        await message.answer(
            f'{name1} у тебя нет столько 💰\nТвой баланс:<code>{balance}</code>💰 ',
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(regexp=r"(^Фут|фут) ?(\d+)?")
async def process_start_command(message: types.Message):
    command_parse = re.compile(r"(^Фут|фут) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    name1 = message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = summ
    data['user_id'] = message.from_user.id
    balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    balance = (balanc[0])
    summ = int(summ)
    if balance >= summ:
        bot_data = await bot.send_dice(message.chat.id, emoji='⚽')
        bot_data = bot_data['dice']['value']
        await sleep(4)
        if bot_data >= 3:
            await message.reply(f'Ты попал(а) в ворота и выиграл(а) - {summ}💰',
                                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET wins = wins + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        else:
            await message.reply(f'Ты промазал(а) и проиграл(а) - {summ}💰',
                                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET games = loses + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
    elif balance < summ:
        await message.answer(
            f'{name1} у тебя нет столько 💰\nТвой баланс:<code>{balance}</code>💰 ',
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(regexp=r"(^Бас|бас|Баскет|баскет) ?(\d+)?")
async def baskeet(message: types.Message):
    command_parse = re.compile(r"(^Бас|бас|Баскет|баскет) ?(\d+)?")
    parsed = command_parse.match(message.text)
    summ = parsed.group(2)
    name1 = message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = summ
    data['user_id'] = message.from_user.id
    balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                  (message.from_user.id, )).fetchone()
    balance = (balanc[0])
    summ = int(summ)
    if balance >= summ:
        bot_data = await bot.send_dice(message.chat.id, emoji='🏀')
        bot_data = bot_data['dice']['value']
        await sleep(4)
        if bot_data >= 4:
            await message.answer(
                f'{name1} ты попал(а) в кольцо и выиграл(а) - {summ}💰',
                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET wins = wins + 1 WHERE id=?',
                (message.from_user.id, ))
        elif bot_data == 3:
            await message.answer(f'{name1} 🗿🗿🗿', parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
        else:
            await message.answer(
                f'{name1} ты промазал(а) и проиграл(а) - {summ}💰',
                parse_mode='html')
            users.cursor.execute(
                """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
                data)
            users.cursor.execute(
                f'UPDATE users SET games = games + 1 WHERE id=?',
                (message.from_user.id, ))
            users.cursor.execute(
                f'UPDATE users SET loses = loses + 1 WHERE id=?',
                (message.from_user.id, ))
            users.connect.commit()
    elif balance < summ:
        await message.answer(
            f'{name1} у тебя нет столько 💰\nТвой баланс:<code>{balance}</code>💰 ',
            parse_mode='html')
        users.connect.commit()


#keys
@dp.message_handler(regexp=r"(^Ключи|ключи) ?(\d+)?")
async def buy_keys(message: types.Message):
    command_parse = re.compile(r"(^Ключи|ключи) ?(\d+)?")
    parsed = command_parse.match(message.text)
    suma = parsed.group(2)
    summ = 250000 * int(suma)
    msg = message
    id = msg['from']['id']
    data = {}
    data["summ"] = summ
    data['user_id'] = message.from_user.id
    data1 = {}
    data1["suma"] = suma
    data1['user_id'] = message.from_user.id
    users.cursor.execute(f"SELECT id FROM users WHERE id = '{id}'")
    name = message.from_user.get_mention(as_html=True)
    balance = users.cursor.execute("SELECT balance from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    balance = (balance[0])
    keys = users.cursor.execute("SELECT keys from users where id = ?",
                                (message.from_user.id, )).fetchone()
    keys = (keys[0])
    if int(balance) >= summ:
        users.cursor.execute(
            """UPDATE users SET balance = balance - :summ WHERE id = :user_id;""",
            data)
        users.cursor.execute(
            """UPDATE users SET keys = keys + :suma WHERE id = :user_id;""",
            data1)
        users.connect.commit()
        await message.reply(
            f'Вы успешно приобрели {suma} 🔑\nПотрачено: <code>{summ}</code> 💰')
        await bot.send_message(
            -1001392898291,
            f'<code>Пользователь {name}, ID: {id}\nПриобрёл: {suma} 🔑\nНа сумму: {summ} 💰</code>'
        )
    else:
        await message.reply(
            f'Для покупки нужно <code>{summ}</code> 💰, а у вас <code>{balance}</code> 💰'
        )


#boxes
@dp.message_handler(lambda message: message.text.lower().startswith(
    ('Купить портфель ', 'купить портфель ')))
async def buy_boxes(message):
    balance = users.cursor.execute("SELECT balance from users where id = ?",
                                   (message.from_user.id, )).fetchone()
    balance = (balance[0])
    try:
        if len(message.text.lower().split()) == 4:
            box_number = message.text.lower().split()[2]
            count = message.text.lower().split()[2]
            box_prices = [0, 10000, 20000,
                          30000]  # 0 = 0, 10000 = 1, 1 = box_number
            if int(count) != 0 and int(count) > 0:
                if int(box_number) >= 1 and int(box_number) <= 3:
                    if int(balance) >= int(
                            box_prices[int(box_number)]) * int(count):
                        btn_accept = types.InlineKeyboardButton(
                            'Подтвердить! ✅',
                            callback_data=
                            f'buy_box_{str(box_number)}_{str(box_prices[int(box_number)])}_{str(count)}'
                        )
                        btn_cancel = types.InlineKeyboardButton(
                            "Отменить! ⛔", callback_data="cancel")
                        kb = types.InlineKeyboardMarkup().add(
                            btn_accept, btn_cancel)
                        b_n = int(box_prices[int(box_number)]) * int(count)
                        await message.reply(
                            f"Нажмите чтобы купить портфель <code>«{str(box_number)}»</code> 📦 в количестве <code>{str(count)}</code> за <code>{b_n}</code> 💰.",
                            parse_mode="html",
                            reply_markup=kb)
                    else:
                        await message.reply("Вам не хватает баланса 💰")
                else:
                    await message.reply(
                        "Число коробок доступных для покупки = <code>3</code> 📦📦📦",
                        parse_mode="html")
            else:
                await message.reply(
                    "Кол-ство коробок не должно равнятся <code>0</code>📦",
                    parse_mode="html")
    except Exception as e:
        await message.reply("""Возможно вы не правильно написали команду
Правильный синтаксис: <code>купить коробку «1-3» «кол-ство портфелей»</code> 📦💰""",
                            parse_mode="html")
        # print(e)


@dp.callback_query_handler(lambda c: c.data.startswith('buy_box_'))
async def buy_box_query(c: types.CallbackQuery):
    box_number = c.data.split("_")[2]
    box_price = c.data.split("_")[3]
    count = c.data.split("_")[4]

    users.cursor.execute(
        f"UPDATE users SET balance = balance - {int(box_price) * int(count)} WHERE id = ?",
        (c.message.reply_to_message.from_user.id, ))
    users.cursor.execute(
        f"UPDATE users SET boxes{box_number} = boxes{box_number} + {count} WHERE id = ?",
        (c.message.reply_to_message.from_user.id, ))
    users.connect.commit()

    b_p = int(box_price) * int(count)

    await c.message.answer(
        f"Вы успешно приобрели портфель <code>«{str(box_number)}»</code> 📦 в количестве <code>{str(count)}</code> за <code>{str(b_p)}</code> 💰.",
        parse_mode="html")
    await bot.delete_message(c.message.chat.id, c.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'cancel')
async def buy_box_query(c: types.CallbackQuery):
    await c.message.answer(f"Отменено!")
    await bot.delete_message(c.message.chat.id, c.message.message_id)


#Взаимодействие с монетами
@dp.message_handler(regexp=r"(^Выдать|выдать) ?(\d+)?")
async def vidat(message: types.Message):
    command_parse = re.compile(r"(^Выдать|выдать) ?(\d+)?")
    parsed = command_parse.match(message.text)
    suma = parsed.group(2)
    name1 = message.from_user.get_mention(as_html=True)
    name2 = message.reply_to_message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = suma
    data['user_id'] = message.reply_to_message.from_user.id
    stts = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    status = (stts[0])
    if str(status) == 'Администратор':
        users.cursor.execute(
            """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
            data)
        await message.answer(
            f"Администратор {name1} выдал пользователю {name2} - <code>{suma}</code> 💰",
            parse_mode='html')
        await bot.send_message(
            -5695410762,
            f'Администратор {name1} выдал пользователю {name2} - <code>{suma}</code>💰'
        )
    elif str(status) == 'Создатель бота':
        users.cursor.execute(
            """UPDATE users SET balance = balance + :suma WHERE id = :user_id;""",
            data)
        await message.answer(
            f"Администратор {name1} выдал пользователю {name2} - <code>{suma}</code> 💰",
            parse_mode='html')
        await bot.send_message(
            -5695410762,
            f'Администратор {name1} выдал пользователю {name2} - <code>{suma}</code>💰'
        )
    else:
        await message.answer(
            f"{name1} у тебя не достаточно прав чтобы выдавать монеты ",
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(regexp=r"(Забрать) ?(\d+)?")
async def vidat(message: types.Message):
    command_parse = re.compile(r"(Забрать) ?(\d+)?")
    parsed = command_parse.match(message.text)
    suma = parsed.group(2)
    name1 = message.from_user.get_mention(as_html=True)
    name2 = message.reply_to_message.from_user.get_mention(as_html=True)
    data = {}
    data["suma"] = suma
    data['user_id'] = message.reply_to_message.from_user.id
    stts = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    status = (stts[0])
    if str(status) == 'Администратор':
        users.cursor.execute(
            """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
            data)
        await message.answer(
            f"Администратор {name1} забрал у пользователя {name2} - <code>{suma}</code>💰",
            parse_mode='html')
        await bot.send_message(
            -5695410762,
            f'{name1} забрал у пользователя {name2} - <code>{suma}</code> 💰')
    elif str(status) == 'Создатель бота':
        users.cursor.execute(
            """UPDATE users SET balance = balance - :suma WHERE id = :user_id;""",
            data)
        await message.answer(
            f"Администратор {name1} забрал у пользователя {name2} - <code>{suma}</code> 💰",
            parse_mode='html')
        await bot.send_message(
            -5695410762,
            f'Администратор {name1} забрал у пользователя {name2} - <code>{suma}</code> 💰'
        )
    else:
        await message.answer(
            f"{name1} у тебя не достаточно прав чтобы забирать монеты ",
            parse_mode='html')
        users.connect.commit()


@dp.message_handler(commands=['setbal'])
async def setbal(message: types.Message):
    args = message.get_args()
    users.cursor.execute("SELECT balance FROM users WHERE id=?",
                         (message.from_user.id, ))
    data = users.cursor.fetchone()
    if data is None:
        await message.reply("Не найден в базе данных!")
    stts = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    status = (stts[0])
    if str(status) == 'Создатель бота':
        reply = message.reply_to_message
        if reply:
            replyuser = reply.from_user
            users.cursor.execute(f'UPDATE users SET balance=? WHERE id=?', (
                args,
                replyuser.id,
            ))
            users.connect.commit()
            await message.reply(
                f"Баланс {replyuser.full_name}, изменён на: {args}💰")
        else:
            await message.reply("Необходим реплай!")
    else:
        return await message.reply(
            "У вас недостаточно прав для того, чтобы менять балансы пользователей!"
        )


#Система рангов
@dp.message_handler(commands=['own', 'owner'], commands_prefix='+!./')
async def ownerka(message: types.Message):
    user_id = message.from_user.id
    name = message.reply_to_message.from_user.full_name
    rank = "Создатель бота"
    stat = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    stat = (stat[0])
    if stat == 'Создатель бота':
        await message.answer(f'✅ | {name} получил(-а) статус «Создатель бота»')
        users.cursor.execute(f'UPDATE users SET status=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
        users.connect.commit()
    else:
        await message.reply('Недостаточно прав ❎')


@dp.message_handler(commands=['adm', 'adminka'], commands_prefix='+!./')
async def adminka(message: types.Message):
    id = message.from_user.id
    name = message.reply_to_message.from_user.full_name
    rank = "Администратор"
    stat = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    stat = (stat[0])
    if stat == 'Создатель бота':
        await message.answer(f'✅ | {name} получил(-а) статус «Администратор»')
        users.cursor.execute(f'UPDATE users SET status=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
        users.connect.commit()
    elif stat == 'Администратор':
        await message.answer(f'✅ | {name} получил(-а) статус «Администратор»')
        users.cursor.execute(f'UPDATE users SET status=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
        users.connect.commit()
    else:
        await message.reply('Вы не можете назначать администраторов ❎')


@dp.message_handler(commands=['vip', 'vipka'], commands_prefix='+!./')
async def vipka(message: types.Message):
    id = message.from_user.id
    name = message.reply_to_message.from_user.full_name
    rank = "Активен"
    vip = users.cursor.execute("SELECT vip from users where id = ?",
                               (message.from_user.id, )).fetchone()
    vip = (vip[0])
    stat = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    stat = (stat[0])
    if stat == 'Создатель бота':
        await message.answer(f'{name} получил(-а) VIP статус ✅')
        users.cursor.execute(f'UPDATE users SET vip=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
        users.connect.commit()
    elif stat == 'Администратор':
        await message.answer(f'{name} получил(-а) VIP статус ✅')
        users.cursor.execute(f'UPDATE users SET vip=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
        users.connect.commit()
    else:
        await message.reply('Вы не можете выдавать VIP статусы ❎')


@dp.message_handler(commands=['sponsor', 'sponsorka'], commands_prefix='+!./')
async def sponsorka(message: types.Message):
    id = message.from_user.id
    name = message.reply_to_message.from_user.full_name
    rank = "Спонсор бота"
    stat = users.cursor.execute("SELECT status from users where user_id = ?",
                                (message.from_user.id, )).fetchone()
    stat = (stat[0])
    if stat == 'Создатель бота':
        await message.answer(f'✅ | {name} получил(-а) статус «Спонсор бота»')
        users.cursor.execute(f'UPDATE users SET status=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
    elif stat == 'Администратор':
        await message.answer(f'✅ | {name} получил(-а) статус «Спонсор бота»')
        users.cursor.execute(f'UPDATE users SET status=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
        users.connect.commit()
    else:
        await message.reply('Вы не можете назначать администраторов ❎')


@dp.message_handler(commands=['member', 'memberka'], commands_prefix='+!./')
async def memberka(message: types.Message):
    id = message.from_user.id
    name = message.reply_to_message.from_user.full_name
    rank = "Пользователь"
    stat = users.cursor.execute("SELECT status from users where id = ?",
                                (message.from_user.id, )).fetchone()
    stat = (stat[0])
    if stat == 'Создатель бота':
        await message.answer(f'{name} разжалован')
        users.cursor.execute(f'UPDATE users SET status=? WHERE id=?', (
            rank,
            message.reply_to_message.from_user.id,
        ))
        users.connect.commit()
    else:
        await message.reply('Недостаточно прав!')


#Команды для модераторов
@dp.message_handler(commands=['мут', 'mute'],
                    commands_prefix='!?./',
                    is_chat_admin=True)
async def mute(message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(message.text.split()[3:])
    except IndexError:
        await message.reply(
            'Не хватает аргументов!\nПример:\n<code>/мут 1 ч причина</code>')
        return
    if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
        await bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            types.ChatPermissions(False),
            until_date=datetime.timedelta(hours=muteint))
        await message.reply(
            f'Модератор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\nЗамутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\nID наказуемого: {message.reply_to_message.from_user.id}\nДлительность мута: {muteint} {mutetype}\nПричина: {comment}'
        )
    if mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
        await bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            types.ChatPermissions(False),
            until_date=datetime.timedelta(minutes=muteint))
        await message.reply(
            f'Модератор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\nЗамутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\nID наказуемого: {message.reply_to_message.from_user.id}\nДлительность мута: {muteint} {mutetype}\nПричина: {comment}'
        )
    if mutetype == "д" or mutetype == "дней" or mutetype == "день":
        await bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            types.ChatPermissions(False),
            until_date=datetime.timedelta(days=muteint))
        await message.reply(
            f'Модератор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\nЗамутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\nID наказуемого: {message.reply_to_message.from_user.id}\nДлительность мута: {muteint} {mutetype}\nПричина: {comment}'
        )


@dp.message_handler(commands=['анмут', 'размут', 'unmute'],
                    commands_prefix='!?./',
                    is_chat_admin=True)
async def unmute(message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    await bot.restrict_chat_member(
        message.chat.id, message.reply_to_message.from_user.id,
        types.ChatPermissions(True, True, True, True))
    await message.reply(
        f'Модератор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\nРазмутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>'
    )


@dp.message_handler(commands=['ban', 'бан', 'кик', 'kick'],
                    commands_prefix='!?./',
                    is_chat_admin=True)
async def ban(message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    comment = " ".join(message.text.split()[1:])
    await bot.kick_chat_member(message.chat.id,
                               message.reply_to_message.from_user.id,
                               types.ChatPermissions(False))
    await message.reply(
        f'Модератор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\nЗабанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\nДлительность: навсегда\nПричина: {comment}'
    )


@dp.message_handler(commands=['разбан', 'unban'],
                    commands_prefix='!?./',
                    is_chat_admin=True)
async def unban(message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    await bot.restrict_chat_member(
        message.chat.id, message.reply_to_message.from_user.id,
        types.ChatPermissions(True, True, True, True))
    await message.reply(
        f'Модератор: <a href="tg://?id={message.from_user.id}">{message.from_user.first_name}</a>\nРазбанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>'
    )


#Удаление сообщения
@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=['del'],
    commands_prefix='!/')
async def delete_message(message: types.Message):
    admins_list = [
        admin.user.id
        for admin in await bot.get_chat_administrators(chat_id=message.chat.id)
    ]
    if message.from_user.id in admins_list:
        msg_id = message.reply_to_message.message_id
        await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)


#Список администраторов чата
@dp.message_handler(commands=["staff"], commands_prefix=['/', '!', '.'])
async def staff_cmd(message: types.Message):
    adm = ""
    if message.chat.type == 'private':
        pass
    else:
        admins_id = [(admin.user.id)
                     for admin in await bot.get_chat_administrators(
                         chat_id=message.chat.id)]
        admins_name = [(admin.user.full_name)
                       for admin in await bot.get_chat_administrators(
                           chat_id=message.chat.id)]
        admin_prefix = [(admin.custom_title)
                        for admin in await bot.get_chat_administrators(
                            chat_id=message.chat.id)]
        for user in admins_id:
            adm += f"<a href='tg://openmessage?user_id={user}'> {admins_name[admins_id.index(user)]}</a> » {admin_prefix[admins_id.index(user)]} " + str(
                '\n')
        await message.answer('<b><i>Администрация чата:</i></b>\n' +
                             str(adm.replace('None', 'Админ')),
                             parse_mode='html')


#led
@dp.message_handler(commands=['led', 'леденец', 'candy'],
                    commands_prefix='+!./')
async def cmd_candy(message: types.Message):
    msg = message
    id = msg['from']['id']
    users.cursor.execute(f"SELECT led_time FROM users WHERE id = '{id}'")
    ltime = users.cursor.fetchone()[0]
    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    name = message.from_user.get_mention(as_html=True)
    q = current_time.strftime('%H:%M:%S')
    a, b, t1, t2 = f'{ltime}'.split(':'), f'{q}'.split(':'), 0, 0
    for i in range(2, -1, -1):
        t1, t2 = t1 + 60**i * int(a[2 - i]), t2 + 60**i * int(b[2 - i])
    a = (86400 - t1) * int(t2 < t1) + t2 - t1 * int(not (t2 < t1))
    if a >= 10800:
        dick = str(randint(1, 10))
        data = {}
        data["rand"] = (dick)
        data['user_id'] = message.from_user.id
        ledenec = users.cursor.execute("SELECT led from users where id = ?",
                                       (message.from_user.id, )).fetchone()
        led = (ledenec[0])
        await message.answer(
            f'{name}, твой член - {led} см. увеличился на {dick} см. 🍭\nСледующая возможность через 3 часа',
            parse_mode='html')
        users.cursor.execute(
            """UPDATE users SET led = led + :rand WHERE id = :user_id;""",
            data)
        users.cursor.execute('UPDATE users SET led_time = ? WHERE id = ?',
                             (q, id))
        users.connect.commit()
    else:
        await message.reply(f'Увеличивать 🍭 можно раз в 3 часа, приходи позже!'
                            )


#marry
inline_btn_marry_y = InlineKeyboardButton('Да 💖',
                                          callback_data='button_marry_y')
button_marry_y = InlineKeyboardMarkup().add(inline_btn_marry_y)

inline_btn_marry_n = InlineKeyboardButton('Нет 💔',
                                          callback_data='button_marry_n')
button_marry_n = InlineKeyboardMarkup().add(inline_btn_marry_n)

button_marry = InlineKeyboardMarkup(row_width=1)
button_marry.row(inline_btn_marry_y, inline_btn_marry_n)

inline_btn_divorce_y = InlineKeyboardButton('Да 💔',
                                            callback_data='button_divorce_y')
button_divorce_y = InlineKeyboardMarkup().add(inline_btn_divorce_y)

inline_btn_divorce_n = InlineKeyboardButton('Нет ❤',
                                            callback_data='button_divorce_n')
button_divorce_n = InlineKeyboardMarkup().add(inline_btn_divorce_n)

button_divorce = InlineKeyboardMarkup(row_width=1)
button_divorce.row(inline_btn_divorce_y, inline_btn_divorce_n)

marry_me = []
marry_rep = []
divorce_me = []
divorce_rep = []


@dp.callback_query_handler(lambda c: c.data == "button_marry_y")
async def callback_marry_y(callback_query: types.CallbackQuery):
    try:
        user = await bot.get_chat(str(marry_me[0]))
    except:
        await bot.answer_callback_query(callback_query.id,
                                        text="Это предложение уже не активно",
                                        show_alert=True)
    replyuser = await bot.get_chat(str(marry_rep[0]))
    name = quote_html(user.full_name)
    rname = quote_html(replyuser.full_name)
    if callback_query.from_user.id == replyuser.id:
        users.cursor.execute(f'UPDATE users SET marry=? WHERE id=?', (
            replyuser.id,
            user.id,
        ))
        users.cursor.execute(f'UPDATE users SET marry_time=? WHERE id=?', (
            time.time(),
            user.id,
        ))

        users.cursor.execute(f'UPDATE users SET marry=? WHERE id=?', (
            user.id,
            replyuser.id,
        ))
        users.cursor.execute(f'UPDATE users SET marry_time=? WHERE id=?', (
            time.time(),
            replyuser.id,
        ))
        users.connect.commit()
        marry_me.clear()
        marry_rep.clear()
        await bot.delete_message(callback_query.message.chat.id,
                                 callback_query.message.message_id)
        await bot.send_message(
            callback_query.message.chat.id,
            f"<a href='tg://user?id={user.id}'>{name}</a> и <a href='tg://user?id={replyuser.id}'>{rname}</a> теперь в браке 💞️"
        )
    else:
        await bot.answer_callback_query(callback_query.id,
                                        text="Не трогай!",
                                        show_alert=True)


@dp.callback_query_handler(lambda c: c.data == "button_marry_n")
async def callback_marry_n(callback_query: types.CallbackQuery):
    try:
        user = await bot.get_chat(str(marry_me[0]))
    except:
        await bot.answer_callback_query(callback_query.id,
                                        text="Это предложение уже не активно",
                                        show_alert=True)
    replyuser = await bot.get_chat(str(marry_rep[0]))
    if callback_query.from_user.id == replyuser.id:
        name = quote_html(user.full_name)
        marry_me.clear()
        marry_rep.clear()
        await bot.delete_message(callback_query.message.chat.id,
                                 callback_query.message.message_id)
        await bot.send_message(
            callback_query.message.chat.id,
            f"<a href='tg://user?id={user.id}'>{name}</a>, сожалеем но вам отказали 💔"
        )
    else:
        await bot.answer_callback_query(callback_query.id,
                                        text="Не трогай!",
                                        show_alert=True)


@dp.callback_query_handler(lambda c: c.data == "button_divorce_y")
async def callback_divorce_y(callback_query: types.CallbackQuery):
    try:
        user = await bot.get_chat(str(divorce_me[0]))
    except:
        await bot.answer_callback_query(callback_query.id,
                                        text="Это предложение уже не активно",
                                        show_alert=True)

    if callback_query.from_user.id == user.id:
        replyuser = await bot.get_chat(str(divorce_rep[0]))
        name = quote_html(user.full_name)
        get = users.cursor.execute("SELECT marry_time FROM users WHERE id=?",
                                   (user.id, )).fetchall()
        mtime = f"{int(get[0][0])}"
        marry_time = time.time() - float(mtime)
        vremya = strftime("%j д %H ч %M мин", gmtime(marry_time))
        users.cursor.execute(f'UPDATE users SET marry=? WHERE id=?', (
            0,
            user.id,
        ))
        users.cursor.execute(f'UPDATE users SET marry_time=? WHERE id=?', (
            0,
            user.id,
        ))

        users.cursor.execute(f'UPDATE users SET marry=? WHERE id=?', (
            0,
            replyuser.id,
        ))
        users.cursor.execute(f'UPDATE users SET marry_time=? WHERE id=?', (
            0,
            replyuser.id,
        ))
        users.connect.commit()
        divorce_me.clear()
        divorce_rep.clear()
        await bot.delete_message(callback_query.message.chat.id,
                                 callback_query.message.message_id)
        await bot.send_message(
            callback_query.message.chat.id,
            f"<a href='tg://user?id={user.id}'>{name}</a>, ваш брак расторгнут!\n"
            f"Он просуществовал {vremya}")
    else:
        await bot.answer_callback_query(callback_query.id,
                                        text="Не трогай!",
                                        show_alert=True)


@dp.callback_query_handler(lambda c: c.data == "button_divorce_n")
async def callback_divorce_n(callback_query: types.CallbackQuery):
    try:
        user = await bot.get_chat(str(divorce_me[0]))
    except:
        await bot.answer_callback_query(callback_query.id,
                                        text="Это предложение уже не активно!",
                                        show_alert=True)
    if callback_query.from_user.id == user.id:
        divorce_me.clear()
        divorce_rep.clear()
        await bot.delete_message(callback_query.message.chat.id,
                                 callback_query.message.message_id)
    else:
        await bot.answer_callback_query(callback_query.id,
                                        text="Не трогай!",
                                        show_alert=True)


#Брак
@dp.message_handler(lambda msg: msg.text.lower() == 'брак')
async def cmd_marry(message: types.Message):
    marry_me.clear()
    marry_rep.clear()
    user = message.from_user
    name = quote_html(user.full_name)
    reply = message.reply_to_message
    if reply:
        replyuser = reply.from_user
        rname = quote_html(replyuser.full_name)
        marry = users.cursor.execute("SELECT marry from users where id = ?",
                                     (message.from_user.id, )).fetchone()
        marry = (marry[0])
        if marry == 0:
            if replyuser.id == user.id:
                return await message.reply(
                    f"Вы не можете сделать брак с самим собой 💔")
            else:
                marry_me.append(user.id)
                marry_rep.append(replyuser.id)
                await bot.send_message(
                    message.chat.id,
                    f"<a href='tg://user?id={replyuser.id}'>{rname}</a>, вы готовы заключить брак с <a href='tg://user?id={user.id}'>{name}</a> ?",
                    reply_markup=button_marry)

        else:
            marry = users.cursor.execute("SELECT marry FROM users WHERE id=?",
                                         (user.id, )).fetchall()
            marred = await bot.get_chat(str(marry[0][0]))
            mname = quote_html(marred.full_name)
            return await message.reply(f"Вы уже в браке с {mname} ❤️")


#Развод
@dp.message_handler(lambda msg: msg.text.lower() == 'развод')
async def cmd_divorce(message: types.Message):
    user = message.from_user
    name = quote_html(user.full_name)
    marry = users.cursor.execute("SELECT marry from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    marry = (marry[0])
    if marry == 0:
        return await message.reply(f"У вас нет брака 💔")
    else:
        marry = users.cursor.execute("SELECT marry FROM users WHERE id=?",
                                     (user.id, )).fetchall()
        marred = await bot.get_chat(str(marry[0][0]))
        mname = quote_html(marred.full_name)
        divorce_me.append(user.id)
        divorce_rep.append(marred.id)
        await bot.send_message(
            message.chat.id,
            f"<a href='tg://user?id={user.id}'>{name}</a>, вы уверены что хотите рассторгнуть брак с <a href='tg://user?id={marred.id}'>{mname}</a> ? 💔",
            reply_markup=button_divorce)


@dp.message_handler(Text(equals="Мой брак"))
async def my_marry(message: types.Message):
    marry = users.cursor.execute("SELECT marry from users where id = ?",
                                 (message.from_user.id, )).fetchone()
    marry = (marry[0])
    if marry == 0:
        await message.reply(f"Вы не в браке!")
    else:
        marry = users.cursor.execute("SELECT marry FROM users WHERE id=?",
                                     (message.from_user.id, )).fetchall()
        marred = await bot.get_chat(marry)
        mname = quote_html(marred.full_name)
        await message.reply(f"Вы в браке с {mname} ❤️")


#echo_message
@dp.message_handler()
async def echo_message(message: types.Message):
    data = {}
    data['chat_id'] = message.chat.id
    data1 = {}
    data1['user_id'] = message.from_user.id
    chats.cursor.execute(
        """UPDATE chats SET chatwords = chatwords + 1 WHERE chatid = :chat_id;""",
        data)
    chats.connect.commit()
    users.cursor.execute(
        """UPDATE users SET words = words + 1 WHERE id = :user_id;""", data1)
    users.connect.commit()

    if message.text.lower() == 'баланс' or message.text.lower() == 'б':
        balanc = users.cursor.execute("SELECT balance from users where id = ?",
                                      (message.from_user.id, )).fetchone()
        balance = (balanc[0])
        await message.reply(f'Ваш баланс: <code>{balance}</code> 💰')

    elif message.text.lower() == '+':
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        data = {}
        data['user_id'] = message.reply_to_message.from_user.id
        respect = users.cursor.execute(
            "SELECT respect from users where id = ?",
            (message.from_user.id, )).fetchone()
        respect = (respect[0])
        if message['reply_to_message']['from']['id'] == message['from']['id']:
            pass
        else:
            users.cursor.execute(
                """UPDATE users SET respect = respect + 1 WHERE id = :user_id;""",
                data)
            rep = message.reply_to_message.from_user.id
            await message.answer(
                f'Ты получил(а) уважение: <a href="tg://user?id={rep}">+1</a>')

    elif message.text.lower() == '++':
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        data = {}
        data['user_id'] = message.reply_to_message.from_user.id
        respect = users.cursor.execute(
            "SELECT respect from users where id = ?",
            (message.from_user.id, )).fetchone()
        respect = (respect[0])
        if message['reply_to_message']['from']['id'] == message['from']['id']:
            pass
        else:
            users.cursor.execute(
                """UPDATE users SET respect = respect + 2 WHERE id = :user_id;""",
                data)
            rep = message.reply_to_message.from_user.id
            await message.answer(
                f'Ты получил(а) уважение: <a href="tg://user?id={rep}">+2</a>')

    elif message.text.lower() == '+++':
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        data = {}
        data['user_id'] = message.reply_to_message.from_user.id
        respect = users.cursor.execute(
            "SELECT respect from users where id = ?",
            (message.from_user.id, )).fetchone()
        respect = (respect[0])
        if message['reply_to_message']['from']['id'] == message['from']['id']:
            pass
        else:
            users.cursor.execute(
                """UPDATE users SET respect = respect + 3 WHERE id = :user_id;""",
                data)
            rep = message.reply_to_message.from_user.id
            await message.answer(
                f'Ты получил(а) уважение: <a href="tg://user?id={rep}">+3</a>')

    elif message.text.lower() == '👍':
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        data = {}
        data['user_id'] = message.reply_to_message.from_user.id
        respect = users.cursor.execute(
            "SELECT respect from users where id = ?",
            (message.from_user.id, )).fetchone()
        respect = (respect[0])
        if message['reply_to_message']['from']['id'] == message['from']['id']:
            pass
        else:
            users.cursor.execute(
                """UPDATE users SET respect = respect + 1 WHERE id = :user_id;""",
                data)
            rep = message.reply_to_message.from_user.id
            await message.answer(
                f'Ты получил(а) уважение: <a href="tg://user?id={rep}">+1</a>')

    elif message.text.lower() == 'поцеловать':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        emoji = ['🥺', '❤', '😊', '🥰', '😘']
        remoji = random.choice(emoji)
        await message.reply(f"{name1}\nпоцеловал(-а) {remoji}\n{name2}")
    elif message.text.lower() == '❤':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.answer(f'{name1} признался(-лась) в любви {name2}')
    elif message.text.lower() == 'всем привет':
        name1 = message.from_user.get_mention(as_html=True)
        await message.answer(
            f"{name1} поприветствовал(-а) всех участников чата ✨",
            parse_mode='html')
    elif message.text.lower() == 'привет всем':
        name1 = message.from_user.get_mention(as_html=True)
        await message.answer(
            f"{name1} поприветствовал(-а) всех участников чата ✨",
            parse_mode='html')
    elif message.text.lower() == 'всем пока':
        name1 = message.from_user.get_mention(as_html=True)
        await message.answer(
            f"{name1} попрощался(-ась) со всеми участниками чата ✨",
            parse_mode='html')
    elif message.text.lower() == 'пока всем':
        name1 = message.from_user.get_mention(as_html=True)
        await message.answer(
            f"{name1} попрощался(-ась) со всеми участниками чата ✨",
            parse_mode='html')
    elif message.text.lower() == 'расенган':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1} ёбнул(-а) расенганом по {name2}",
                            parse_mode='html')
    elif message.text.lower() == 'гетсуга':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1} использовал(-а) гетсугу на {name2}",
                            parse_mode='html')
    elif message.text.lower() == 'чмок':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1} чмокнул(-а) {name2}", parse_mode='html')
    elif message.text.lower() == 'чпок':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1} чпокнул(-а) {name2}", parse_mode='html')
    elif message.text.lower() == 'пнуть':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1} пнул(-а) {name2}", parse_mode='html')
    elif message.text.lower() == 'лизнуть':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1} лизнул(-а) {name2}", parse_mode='html')
    elif message.text.lower() == 'банкай':
        name1 = message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1}, применил(-а) банкай!",
                            parse_mode='html')
    elif message.text.lower() == 'обнять':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        emoji = ['🥺', '❤', '😊', '🥰', '😘']
        remoji = random.choice(emoji)
        await message.reply(f"{name1}\nобнял(-а) {remoji}\n{name2}",
                            parse_mode='html')
    elif message.text.lower() == 'заебашить':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        e = ['лопатой', 'арматурой', 'резиновым хуём']
        i = random.choice(e)
        await message.reply(f"{name1}\nзаебашил(-а) {i}\n{name2}",
                            parse_mode='html')
    elif message.text.lower() == 'отсосать':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1}\nотсосал(-а) у\n{name2}",
                            parse_mode='html')
    elif message.text.lower() == 'отлизать':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1}\nотлизал(-а) у\n{name2}",
                            parse_mode='html')
    elif message.text.lower() == 'минет':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1} сделал(-а) минет {name2}",
                            parse_mode='html')
    elif message.text.lower() == 'тык':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        t = ['доебался(-ась) до', 'тыкнул(-а)']
        g = random.choice(t)
        await message.reply(f"{name1} {g} {name2}", parse_mode='html')
    elif message.text.lower() == 'отдаться':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1}\nотдался(-ась)\n{name2}",
                            parse_mode='html')
    elif message.text.lower() == 'раздеть':
        name1 = message.from_user.get_mention(as_html=True)
        name2 = message.reply_to_message.from_user.get_mention(as_html=True)
        await message.reply(f"{name1}\nраздел(-а)\n{name2}", parse_mode='html')


if __name__ == "__main__":
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
