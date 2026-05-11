from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import CallbackQueryHandler

api_id = 36794033
api_hash = "f0f1a2dcdfc1f012ed85f41a4e1ea1ef"
bot_token = "7959585410:AAHfx4fDgbjb6LuAopcyKc9Kjwv8lyv7Kzk"

# PRIVATE CHANNEL ID
CHANNEL = -1003974281028

# PRIVATE INVITE LINK
CHANNEL_LINK = "https://t.me/+jGFoT7DWwhczNzM1"

# ADMIN USER ID
ADMIN_ID = 1829824114

UPI_ID = "zaincarder@axl"

app = Client(
    "storebot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

user_data = {}

# ================= FORCE JOIN =================

async def is_joined(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================= START =================

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):

    joined = await is_joined(client, message.from_user.id)

    if not joined:
        buttons = [
            [
                InlineKeyboardButton(
                    "🔥 JOIN CHANNEL 🔥",
                    url="https://t.me/+jGFoT7DWwhczNzM1"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ JOINED",
                    callback_data="check_join"
                )
            ]
        ]

        await message.reply_photo(
            photo="https://graph.org/file/8d4e2e7f6d4f0d4d1d4fd.jpg",
            caption="""
🔥 Welcome To Carder Zone 🔥

⚠️ Pehle Channel Join Karo
Uske baad Store Open Hoga
""",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    buttons = [
        [
            InlineKeyboardButton("🎮 BGMI UC", callback_data="bgmi")
        ],
        [
            InlineKeyboardButton("💳 CREDIT CARD", callback_data="cc")
        ],
        [
            InlineKeyboardButton("🎁 GIFT CARD", callback_data="gift")
        ],
        [
            InlineKeyboardButton("☠️ HACKS", callback_data="hack")
        ]
    ]

    await message.reply_text(
        "🔥 Welcome To Carder Zone Store 🔥",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ================= CHECK JOIN =================

@app.on_callback_query(filters.regex("check_join"))
async def check_join(client, callback_query):

    joined = await is_joined(client, callback_query.from_user.id)

    if not joined:
        await callback_query.answer(
            "❌ Channel Join Nahi Kiya",
            show_alert=True
        )
        return

    buttons = [
        [
            InlineKeyboardButton("🎮 BGMI UC", callback_data="bgmi")
        ],
        [
            InlineKeyboardButton("💳 CREDIT CARD", callback_data="cc")
        ],
        [
            InlineKeyboardButton("🎁 GIFT CARD", callback_data="gift")
        ],
        [
            InlineKeyboardButton("☠️ HACKS", callback_data="hack")
        ]
    ]

    await callback_query.message.reply_text(
        "🔥 Store Opened 🔥",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ================= BGMI =================

@app.on_callback_query(filters.regex("bgmi"))
async def bgmi(client, callback_query):

    buttons = [
        [
            InlineKeyboardButton(
                "8100 UC - ₹3000",
                callback_data="buy_8100"
            )
        ],
        [
            InlineKeyboardButton(
                "18000 UC - ₹5000",
                callback_data="buy_18000"
            )
        ]
    ]

    await callback_query.message.reply_text(
        "🎮 BGMI UC PACKS",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ================= CREDIT CARD =================

@app.on_callback_query(filters.regex("cc"))
async def cc(client, callback_query):

    text = """
💳 CREDIT CARDS

15$ = ₹1455
Balance 400$-450$

20$ = ₹1940
Balance 4500$

35$ = ₹3395
Balance 6780$

50$ = ₹4850
Balance 800$-900$

100$ = ₹9700
Balance 900$-2000$
"""

    await callback_query.message.reply_text(text)

# ================= GIFT CARD =================

@app.on_callback_query(filters.regex("gift"))
async def gift(client, callback_query):

    text = """
🎁 GIFT CARDS

15$ = ₹1455
Balance 3000

20$ = ₹1940
Balance 4500

35$ = ₹3395
Balance 6780
"""

    await callback_query.message.reply_text(text)

# ================= HACK =================

@app.on_callback_query(filters.regex("hack"))
async def hack(client, callback_query):

    user = callback_query.from_user

    await client.send_message(
        ADMIN_ID,
        f"☠️ Hack Request From @{user.username}"
    )

    await callback_query.message.reply_text(
        "✅ Hack Team Will Contact You"
    )

# ================= BUY =================

@app.on_callback_query(filters.regex("buy_"))
async def buy(client, callback_query):

    user_id = callback_query.from_user.id

    if "8100" in callback_query.data:
        product = "8100 UC"
        price = "3000"
    else:
        product = "18000 UC"
        price = "5000"

    user_data[user_id] = {
        "product": product,
        "price": price
    }

    await callback_query.message.reply_text(
        f"""
🎮 Product: {product}

💰 Amount: ₹{price}

🆔 Ab BGMI UID Bhejo
"""
    )

# ================= USER MESSAGE =================

@app.on_message(filters.private)
async def user_message(client, message):

    user_id = message.from_user.id
    message_text = message.text

    if user_id not in user_data:
        return

    data = user_data[user_id]

    # ===== UID =====

    if "uid" not in data and "UC" in data["product"]:

        data["uid"] = message_text

        await message.reply_text(
            "🎮 Ab BGMI Username Bhejo"
        )

        return

    # ===== USERNAME =====

    if "username" not in data and "uid" in data:

        data["username"] = message_text

        await message.reply_text(
            f"""
💰 Amount: ₹{data['price']}

🏦 UPI ID:
{UPI_ID}

📥 Payment Karke UTR Bhejo
"""
        )

        return

    # ===== UTR =====

    if "utr" not in data:

        data["utr"] = message_text

        buttons = [
            [
                InlineKeyboardButton(
                    "✅ Approve",
                    callback_data=f"approve_{user_id}"
                ),

                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject_{user_id}"
                )
            ]
        ]

        text = f"""
🛒 NEW ORDER

🎮 Product: {data['product']}

💰 Amount: ₹{data['price']}

🔢 UTR: {data['utr']}
"""

        if "uid" in data:
            text += f"\n🎮 UID: {data['uid']}"

        if "username" in data:
            text += f"\n👤 BGMI Username: {data['username']}"

        await client.send_message(
            ADMIN_ID,
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        await message.reply_text(
            "⌛ Payment Verifying..."
        )

# ================= APPROVE =================

@app.on_callback_query(filters.regex("approve_"))
async def approve(client, callback_query):

    user_id = int(callback_query.data.split("_")[1])

    await client.send_message(
        user_id,
        "✅ Payment Successful\n\n🎮 Order Confirmed"
    )

    await callback_query.message.edit_text(
        "✅ Payment Approved"
    )

# ================= REJECT =================

@app.on_callback_query(filters.regex("reject_"))
async def reject(client, callback_query):

    user_id = int(callback_query.data.split("_")[1])

    await client.send_message(
        user_id,
        "❌ Wrong UTR Number\n\nTry Again"
    )

    await callback_query.message.edit_text(
        "❌ Payment Rejected"
    )

app.run()
