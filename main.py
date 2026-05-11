from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = 36794033
api_hash = "f0f1a2dcdfc1f012ed85f41a4e1ea1ef"
bot_token = "7959585410:AAHfx4fDgbjb6LuAopcyKc9Kjwv8lyv7Kzk"

CHANNEL =-1003974281028

app = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):

    user_id = message.from_user.id

    try:
        member = await client.get_chat_member(CHANNEL, user_id)

        if member.status in ["member", "administrator", "creator"]:
            await message.reply_text("✅ Welcome")

    except:
        buttons = [
            [
                InlineKeyboardButton(
                    "Join Channel",
                    url="https://t.me/+jGFoT7DWwhczNzM1"
                )
            ]
        ]

        await message.reply_text(
            "❌ Pehle channel join karo",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

app.run()
