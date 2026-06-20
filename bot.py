    import asyncio
import logging
import sys
from datetime import timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions

# Твій токен вже вшитий прямо в код
TOKEN = "8429257687:AAFmMnFcwi3C0FADyFhmDrbKy9Exvuo4dLs"

dp = Dispatcher()
bot = Bot(token=TOKEN)

# Перевірка, чи є користувач адміном
async def is_admin(message: types.Message) -> bool:
    member = await message.chat.get_member(message.from_user.id)
    return member.status in ["administrator", "creator"]

# Команда /ban (відповіддю на повідомлення порушника)
@dp.message(Command("ban"))
async def ban_user(message: types.Message):
    if not await is_admin(message):
        await message.reply("❌ У тебе немає прав для цієї команди.")
        return

    if not message.reply_to_message:
        await message.reply("❌ Ця команда має бути відповіддю (reply) на повідомлення порушника!")
        return

    user_id = message.reply_to_message.from_user.id
    try:
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
        await message.reply(f"💥 Користувача {message.reply_to_message.from_user.full_name} заблоковано!")
    except Exception as e:
        await message.reply(f"❌ Не вдалося забанити: {e}")

# Команда /mute (на 10 хвилин відповіддю на повідомлення)
@dp.message(Command("mute"))
async def mute_user(message: types.Message):
    if not await is_admin(message):
        await message.reply("❌ У тебе немає прав для цієї команди.")
        return

    if not message.reply_to_message:
        await message.reply("❌ Ця команда має бути відповіддю (reply) на повідомлення порушника!")
        return

    user_id = message.reply_to_message.from_user.id
    permissions = ChatPermissions(can_send_messages=False)
    until_date = timedelta(minutes=10)

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=permissions,
            until_date=until_date
        )
        await message.reply(f"🤫 Користувача {message.reply_to_message.from_user.full_name} заглушено на 10 хвилин.")
    except Exception as e:
        await message.reply(f"❌ Не вдалося замутити: {e}")

# Команда /unmute (зняти мут)
@dp.message(Command("unmute"))
async def unmute_user(message: types.Message):
    if not await is_admin(message):
        return

    if not message.reply_to_message:
        await message.reply("❌ Дай відповідь на повідомлення того, кого треба розмутити.")
        return

    user_id = message.reply_to_message.from_user.id
    permissions = ChatPermissions(can_send_messages=True)

    try:
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=permissions)
        await message.reply(f"🔊 З користувача {message.reply_to_message.from_user.full_name} знято обмеження.")
    except Exception as e:
        await message.reply(f"❌ Не вдалося розмутити: {e}")

async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
