from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 36794033
API_HASH = "f0f1a2dcdfc1f012ed85f41a4e1ea1ef"
BOT_TOKEN = "7959585410:AAHfx4fDgbjb6LuAopcyKc9Kjwv8lyv7Kzk"

ADMIN_ID = 1829824114
FORCE_CHANNEL = -1003974281028
UPI_ID = "zayncarder@axl"

app = Client(
    "shop_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user_data = {}

# ================= FORCE JOIN =================

async def joined(client, user_id):
    try:
        member = await client.get_chat_member(
            chat_id=FORCE_CHANNEL,
            user_id=user_id
        )

        if member.status in ["member", "administrator", "creator"]:
            return True

        return False
    except Exception:
        return False

# ================= START =================

@app.on_message(filters.command("start"))
async def start(client, message):
    ok = await joined(client, message.from_user.id)

    if not ok:
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url="https://t.me/zain_carder_zone"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ Joined",
                    callback_data="check_join"
                )
            ]
        ])

        return await message.reply_text(
            "⚠️ Pehle Channel Join Karo",
            reply_markup=buttons
        )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 BGMI UC", callback_data="bgmi")],
        [InlineKeyboardButton("💳 Credit Cards", callback_data="cc")],
        [InlineKeyboardButton("🎁 Gift Cards", callback_data="gift")]
    ])

    await message.reply_text(
        "🔥 Welcome To Store",
        reply_markup=buttons
    )

# ================= CHECK JOIN =================

@app.on_callback_query(filters.regex("check_join"))
async def check_join(client, callback_query):
    ok = await joined(client, callback_query.from_user.id)

    if ok:
        await callback_query.message.delete()
        await start(client, callback_query.message)
    else:
        await callback_query.answer(
            "❌ Channel Join Nahi Kiya",
            show_alert=True
        )

# ================= BGMI =================

@app.on_callback_query(filters.regex("bgmi"))
async def bgmi(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("8100 UC - ₹3000", callback_data="buy_8100")],
        [InlineKeyboardButton("18000 UC - ₹5000", callback_data="buy_18000")]
    ])
    await callback_query.message.reply_text("🎮 Select UC Package", reply_markup=buttons)

# ================= CREDIT CARD =================

@app.on_callback_query(filters.regex("cc"))
async def cc(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("15$ CC - ₹1455", callback_data="buy_cc15")],
        [InlineKeyboardButton("20$ CC - ₹1940", callback_data="buy_cc20")]
    ])
    await callback_query.message.reply_text("💳 Select Credit Card", reply_markup=buttons)

# ================= GIFT CARD =================

@app.on_callback_query(filters.regex("gift"))
async def gift(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("15$ Gift - ₹1455", callback_data="buy_gift15")],
        [InlineKeyboardButton("20$ Gift - ₹1940", callback_data="buy_gift20")]
    ])
    await callback_query.message.reply_text("🎁 Select Gift Card", reply_markup=buttons)

# ================= BUY SYSTEM =================

@app.on_callback_query(filters.regex("^buy_"))
async def buy(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    products = {
        "buy_8100": {"product": "8100 UC", "price": "3000", "type": "bgmi"},
        "buy_18000": {"product": "18000 UC", "price": "5000", "type": "bgmi"},
        "buy_cc15": {"product": "15$ Credit Card", "price": "1455", "type": "card"},
        "buy_cc20": {"product": "20$ Credit Card", "price": "1940", "type": "card"},
        "buy_gift15": {"product": "15$ Gift Card", "price": "1455", "type": "gift"},
        "buy_gift20": {"product": "20$ Gift Card", "price": "1940", "type": "gift"}
    }

    if data not in products:
        return

    item = products[data]
    user_data[user_id] = {"product": item["product"], "price": item["price"], "step": "waiting"}

    if item["type"] == "bgmi":
        user_data[user_id]["step"] = "uid"
        await callback_query.message.reply_text(f"🎮 Product: {item['product']}\n💰 Amount: ₹{item['price']}\n\n🆔 BGMI UID Bhejo")
    else:
        user_data[user_id]["step"] = "utr"
        await callback_query.message.reply_text(f"🛒 Product: {item['product']}\n💰 Amount: ₹{item['price']}\n\n🏦 UPI ID:\n`{UPI_ID}`\n\n📥 Payment Karke UTR Bhejo")

# ================= TEXT HANDLER =================

@app.on_message(filters.text & filters.private)
async def text_handler(client, message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return

    data = user_data[user_id]
    if data["step"] == "uid":
        user_data[user_id]["uid"] = message.text
        user_data[user_id]["step"] = "utr"
        await message.reply_text(f"✅ UID Saved\n\n🏦 UPI ID:\n`{UPI_ID}`\n\n📥 Payment Karke UTR Bhejo")
    elif data["step"] == "utr":
        user_data[user_id]["utr"] = message.text
        user_data[user_id]["step"] = "screenshot"
        await message.reply_text("📸 Ab Payment Screenshot Send Karo")

# ================= SCREENSHOT =================

@app.on_message(filters.photo & filters.private)
async def photo_handler(client, message):
    user_id = message.from_user.id
    if user_id not in user_data or user_data[user_id]["step"] != "screenshot":
        return

    data = user_data[user_id]
    caption = f"🛒 New Order\n\n👤 User: {message.from_user.mention}\n🆔 User ID: {user_id}\n\n📦 Product: {data['product']}\n💰 Price: ₹{data['price']}\n\n🎮 UID: {data.get('uid', 'N/A')}\n💳 UTR: {data['utr']}"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_{user_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
        ]
    ])

    await client.send_photo(ADMIN_ID, photo=message.photo.file_id, caption=caption, reply_markup=buttons)
    await message.reply_text("✅ Payment Submitted")
    user_data[user_id]["step"] = "done"

# ================= ACCEPT/REJECT =================

@app.on_callback_query(filters.regex("^(accept|reject)_"))
async def handle_order(client, callback_query):
    if callback_query.from_user.id != ADMIN_ID:
        return

    action, user_id = callback_query.data.split("_")
    user_id = int(user_id)

    if action == "accept":
        await client.send_message(user_id, "✅ Payment Verified\n\nOrder Approved")
        await callback_query.message.edit_caption(callback_query.message.caption + "\n\n✅ ACCEPTED")
    else:
        await client.send_message(user_id, "❌ Payment Rejected")
        await callback_query.message.edit_caption(callback_query.message.caption + "\n\n❌ REJECTED")

print("Bot Started...")
app.run()
