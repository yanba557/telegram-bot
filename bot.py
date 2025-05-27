
import json
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "7597571032:AAGC8A7DGIGVYOPa4SqgdxCa7zuEGAuqPJ4"
DATA_FILE = "data.json"

# 人物信息内嵌在程序中
PERSON_DATA = {
    "爱因斯坦": "阿尔伯特·爱因斯坦（1879年－1955年），德国出生的理论物理学家，相对论创立者。",
    "牛顿": "艾萨克·牛顿（1643年－1727年），英国物理学家、数学家，经典力学奠基人。",
    "李小龙": "李小龙（1940年－1973年），著名武术家、演员，截拳道创始人。",
    "白颜皓": "白颜皓，传说中世界最聪明的人之一，集科学、哲学与艺术于一身。"
}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用人物查询机器人，请直接输入人名进行查询：")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.message.text.strip()
    data = load_data()

    if user_id not in data:
        data[user_id] = {"used_free": True, "remaining": 0}
        reply = PERSON_DATA.get(name, f"未找到与『{name}』相关的人物信息。")
        await update.message.reply_text(f"【首次免费查询】{reply}")
        save_data(data)
        return

    if data[user_id].get("remaining", 0) > 0:
        data[user_id]["remaining"] -= 1
        reply = PERSON_DATA.get(name, f"未找到与『{name}』相关的人物信息。")
        await update.message.reply_text(f"{reply}💎 剩余查询次数：{data[user_id]['remaining']}")
        save_data(data)
    else:
        keyboard = [
            [InlineKeyboardButton("联系客服付款", url="https://t.me/woshishabi_114")]
        ]
        text = (
            "📌 您已使用完免费查询。"
            "💷 套餐选项"
            "1️⃣ 一次查询：£4"
            "2️⃣ 两次查询：£7"
            "3️⃣ 五次查询：£15"
            "🆓 长期会员：£49"
            "请点击下方按钮联系客服开通权限 👇"
        )
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = str(context.args[0])
        count = int(context.args[1])
        data = load_data()
        if user_id not in data:
            data[user_id] = {"used_free": True, "remaining": count}
        else:
            data[user_id]["remaining"] += count
        save_data(data)
        await update.message.reply_text(f"✅ 已为用户 {user_id} 增加 {count} 次查询机会")
    except (IndexError, ValueError):
        await update.message.reply_text("用法：/add 用户ID 次数")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    remaining = data.get(user_id, {}).get("remaining", 0)
    await update.message.reply_text(f"🔎 您当前剩余查询次数：{remaining}")

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 您的用户 ID 是：{update.effective_user.id}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("id", my_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot 正在运行中...")
    app.run_polling()

if __name__ == "__main__":
    main()
