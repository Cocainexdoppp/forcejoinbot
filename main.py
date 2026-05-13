from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= CONFIGURATION =================
API_ID = 36794033
API_HASH = "f0f1a2dcdfc1f012ed85f41a4e1ea1ef"
BOT_TOKEN = "7959585410:AAHfx4fDgbjb6LuAopcyKc9Kjwv8lyv7Kzk"

ADMIN_ID = 1829824114
FORCE_CHANNEL = -1003974281028
UPI_ID = "zayncarder@axl"

app = Client("shop_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_data = {}

# ================= FORCE JOIN FUNCTION =================
@app.on_callback_query(filters.regex("check_join"))
async def check_join_fix(client, callback_query):
    user_id = callback_query.from_user.id
    is_ok = await joined(client, user_id)
    
    if is_ok:
        await callback_query.answer("✅ Welcome! Aapne join kar liya hai.", show_alert=True)
        await callback_query.message.delete() # Join wala message delete karega
        await start(client, callback_query.message) # Phir se start menu dikhayega
    else:
        await callback_query.answer("❌ Abhi tak join nahi kiya! Pehle join karein.", show_alert=True)

# ================= START COMMAND =================
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    if not await joined(client, user_id):
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/zain_carder_zone")],
            [InlineKeyboardButton("✅ Joined", callback_data="check_join")]
        ])
        return await message.reply_text("⚠️ Pehle Channel Join Karo", reply_markup=buttons)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 BGMI UC", callback_data="bgmi")],
        [InlineKeyboardButton("💳 Credit Cards", callback_data="cc")],
        [InlineKeyboardButton("🎁 Gift Cards", callback_data="gift")]
    ])
    await message.reply_text("🔥 Welcome To Store", reply_markup=buttons)

# ================= MENU HANDLERS =================
@app.on_callback_query(filters.regex("^(bgmi|cc|gift)$"))
async def menus(client, callback_query):
    data = callback_query.data
    if data == "bgmi":
        buttons = [[InlineKeyboardButton("8100 UC - ₹3000", callback_data="buy_8100")],
                   [InlineKeyboardButton("18000 UC - ₹5000", callback_data="buy_18000")]]
        text = "🎮 Select UC Package"
    elif data == "cc":
        buttons = [[InlineKeyboardButton("15$ CC - ₹1455", callback_data="buy_cc15")],
                   [InlineKeyboardButton("20$ CC - ₹1940", callback_data="buy_cc20")]]
        text = "💳 Select Credit Card"
    else:
        buttons = [[InlineKeyboardButton("15$ Gift - ₹1455", callback_data="buy_gift15")],
                   [InlineKeyboardButton("20$ Gift - ₹1940", callback_data="buy_gift20")]]
        text = "🎁 Select Gift Card"
    
    await callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

# ================= BUY SYSTEM (LATEST FIX) =================
@app.on_callback_query(filters.regex("^buy_"))
async def buy_handler(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    products = {
        "buy_8100": {"name": "8100 UC", "price": "3000", "is_bgmi": True},
        "buy_18000": {"name": "18000 UC", "price": "5000", "is_bgmi": True},
        "buy_cc15": {"name": "15$ Credit Card", "price": "1455", "is_bgmi": False},
        "buy_cc20": {"name": "20$ Credit Card", "price": "1940", "is_bgmi": False},
        "buy_gift15": {"name": "15$ Gift Card", "price": "1455", "is_bgmi": False},
        "buy_gift20": {"name": "20$ Gift Card", "price": "1940", "is_bgmi": False}
    }

    item = products[data]
    user_data[user_id] = {"product": item["name"], "price": item["price"], "is_bgmi": item["is_bgmi"]}

    if item["is_bgmi"]:
        user_data[user_id]["step"] = "uid"
        await callback_query.message.reply_text(f"🎮 Product: {item['name']}\n💰 Amount: ₹{item['price']}\n\n🆔 BGMI UID Bhejo:")
    else:
        # Gift Card/CC ke liye UID skip, direct Payment
        user_data[user_id]["step"] = "utr"
        await callback_query.message.reply_text(f"🛒 Product: {item['name']}\n💰 Amount: ₹{item['price']}\n\n🏦 UPI ID: `{UPI_ID}`\n\n📥 Payment karke UTR Number bhejo:")

# ================= TEXT HANDLER =================
@app.on_message(filters.text & filters.private)
async def handle_text(client, message):
    user_id = message.from_user.id
    if user_id not in user_data: return
    step = user_data[user_id].get("step")

    if step == "uid":
        user_data[user_id]["uid"] = message.text
        user_data[user_id]["step"] = "utr"
        await message.reply_text(f"✅ UID Saved\n\n🏦 UPI ID: `{UPI_ID}`\n\n📥 Payment karke UTR Bhejo:")
    
    elif step == "utr":
        user_data[user_id]["utr"] = message.text
        user_data[user_id]["step"] = "screenshot"
        await message.reply_text("📸 Ab Payment Screenshot Send Karo")

# ================= PHOTO HANDLER =================
@app.on_message(filters.photo & filters.private)
async def handle_photo(client, message):
    user_id = message.from_user.id
    if user_id not in user_data or user_data[user_id].get("step") != "screenshot": return

    data = user_data[user_id]
    uid_info = f"🎮 UID: `{data['uid']}`" if data.get("is_bgmi") else "🎮 UID: Not Required"
    
    caption = (f"🛒 **New Order**\n\n👤 User: {message.from_user.mention}\n🆔 ID: `{user_id}`\n"
               f"📦 Product: {data['product']}\n💰 Price: ₹{data['price']}\n{uid_info}\n💳 UTR: `{data['utr']}`")

    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Accept", callback_data=f"accept_{user_id}"),
                                     InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")]])

    await client.send_photo(ADMIN_ID, photo=message.photo.file_id, caption=caption, reply_markup=buttons)
    await message.reply_text("✅ Payment Submitted! Admin verify kar raha hai.")
    user_data[user_id]["step"] = "done"

# ================= ADMIN ACTIONS & REST =================
@app.on_callback_query(filters.regex("^(accept|reject|check_join)_"))
async def callback_rest(client, callback_query):
    data = callback_query.data
    if data == "check_join":
        if await joined(client, callback_query.from_user.id):
            await callback_query.message.delete()
            await start(client, callback_query.message)
        else:
            await callback_query.answer("❌ Join Nahi Kiya", show_alert=True)
    elif callback_query.from_user.id == ADMIN_ID:
        action, target_id = data.split("_")
        msg = "✅ Approved" if action == "accept" else "❌ Rejected"
        await client.send_message(int(target_id), f"Aapka payment {msg} ho gaya hai.")
        await callback_query.message.edit_caption(callback_query.message.caption + f"\n\n{msg}")

print("Bot Started Successfully!")
app.run()
