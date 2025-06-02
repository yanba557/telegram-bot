
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

BOT_TOKEN = "7597571032:AAGh7iblj5vIO5WT2SjOKHmXL2W1FGyKWX4"
DATA_FILE = "data.json"

# 人物信息库
PERSON_DATA = {
    "Hassan Abdelhadi": """Name: Hassan Abdelhadi
                    DOB: 16/3/2011
                    Address: 111A, Inderwick Road, London N8 9LA
                    Dad: Mohamed Abdelhadi
                    07969202793
                    mohamedhadiuk@yahoo.co.uk""",
    "Somtochukwu Agom": """Name: Somtochukwu Agom
                    DOB: 30/9/2010
                    Address: 39A Bronhill Terrace, Lansdowne Road, London N17 0LN
                    Mom: Suzanne Agom
                    07984196124
                    ijemaloko2@gmail.com""",
    "Nicolas Araujo": """Name: Nicolas Araujo
                    DOB: 6/5/2011
                    Address: 58, Scotland Green,London N17 9TU
                    Mom: Camilla Callabria
                    07494961490
                    camillacallabria@hotmail.com""",
    "Aydin Atchia": """Name: Aydin Atchia
                    DOB: 14/8/2011
                    Address: 28, Dunloe Avenue, London N17 6LA
                    Mom: Marieve Cotte
                    07505761908
                    valatchia@icloud.com""",
    "Thabo Atkinson": """Name: Thabo Atkinson
                    DOB: 30/3/2011
                    Address: Flat 19, Ashridge Court, Reservoir Road, London N14 4BE
                    Mom: Nathlee Atkinson
                    07479310663
                    nathlee.walters@gmail.com""",
    "Yanhao Bai": """Name: Yanhao Bai
                    DOB: 13/3/2011
                    Address: Flat 33, Blenheim Mansions 3, Mary Neuner Road, London N8 0EZ
                    Dad: Weijun Bai
                    07961234778
                    ndbwj@162.com""",
    "George Brunnen": """Name: George Brunnen
                    DOB: 6/4/2011
                    Address: Flat 9, Bruce Castle Court, Lordship Lane, London N17 6RR
                    Mom: Lucy Brunnen
                    07989978811
                    lucymassy@gmail.com""",
    "Shermaine Corre": """Name: Shermaine Corre
                    DOB: 9/1/2011
                    Address: 4, Blake Road, London N11 2AA
                    Mom: Shirley Corre
                    07398853048
                    shirley.corre@yahoo.com""",
    "Ciana Dell-Samuels": """Name: Ciana Dell-Samuels
                    DOB: 3/9/2010
                    Address: 13, Kimberley Gardens, London N4 1LB
                    Mom: Carlena Daley-Samuels
                    07377410833
                    daleycarlena724@gmail.com""",
    "Kyana Foster": """Name: Kyana Foster
                    DOB: 15/7/2011
                    Address: 7, Baronet Road, London N17 0LU
                    Mom: Yhanieke Coke
                    07415261976
                    yhanieke.coke@outlook.com""",
    "Erin Guan": """Name: Erin Guan
                    DOB: 2/11/2010
                    Address: 111 Alexandra Road, Hornsey, London N8 0LG
                    Mom: Li Ping Guan
                    07908769509
                    guanliping1@yahoo.co.uk""",
    "Lucas Guo": """Name: Lucas Guo
                    DOB: 15/6/2011
                    Address: 5, Lancaster Road, London N18 1HP
                    Mom: Xueqin Xue
                    07537982008
                    silent7715@hotmail.com""",
    "Shiloh Lombadi": """Name: Shiloh Lombadi
                    DOB: 26/11/2010
                    Address: Higham Road, London N17 6NN
                    Mom: Mikato Corinne
                    07887982706
                    corinnemikato@gmail.com""",
    "Isaac Medina Sangoquiza": """Name: Isaac Medina Sangoquiza
                    DOB: 22/5/2011
                    Address: Flat 69, Mountview Court, Green Lanes, London N8 0SH
                    Mom: Holanda Sangoquiza
                    07832920835
                    alexandra.llosa@hotmail.com""",
    "Elisabeth Mina": """Name: Elisabeth Mina
                    DOB: 29/4/2011
                    Address: 23, Gascoigne Close, London N17 8BA
                    Mom: Angel Mina
                    07484638756
                    angelmina53@gmail.com""",
    "Nisanur Ogul": """Name: Nisanur Ogul
                    DOB: 15/8/2011
                    Address: Flat 74, Martlesham, Adams Road, London N17 6HT
                    Mom: Nursel Ogul
                    07404880336
                    nnursel47@hotmail.com""",
    "Martin Ozbay": """Name: Martin Ozbay
                    DOB: 6/2/2011
                    Address: 6, Ivy Lodge 282, Holly Park, London N4 4AQ
                    Mom: Mergan Ozbay
                    07823488888
                    ayhanozbay@hotmail.co.uk""",
    "Yazzed Parker": """Name: Yazzed Parker
                    DOB: 25/2/2011
                    Address: 55, Halefield Road, London N17 9XR
                    Mom: Hawa Jalloh
                    07902552440
                    hawajalloh12@hotmail.com""",
    "Jonathan Reynolds": """Name: Jonathan Reynolds
                    DOB: 4/12/2010
                    Address: 23, Etherley Road, London N15 3AL
                    Mom: Sally Reynolds
                    07913115872
                    sallyreynolds27@yahoo.co.uk""",
    "Ethan Carlyle Salicob": """Name: Ethan Carlyle Salicob
                    DOB: 13/8/2011
                    Address: 84, Wood Vale, London N10 3DN""",
    "Khiarna Sammy": """Name: Khiarna Sammy
                    DOB: 1/3/2011
                    Address: 15 Colorado Apartments, Great Amwell Lane, London N8 7NH
                    Mom: Nicola Sammy
                    07939989072
                    nicola.sammy@yahoo.co.uk""",
    "Ivan Swinhoe": """Name: Ivan Swinhoe
                    DOB: 17/9/2010
                    Address: 14, Hampden Road, London N17 0AY
                    Mom: Emma Swinhoe
                    07817905166
                    emma.swinhoe@gmail.com""",
    "Elanur Titiz": """Name: Elanur Titiz
                    DOB: 3/10/2010
                    Address: 24, Willow Walk, London N15 3DQ
                    Mom: Inci Titiz
                    07429145228
                    inci@live.co.uk""",
    "Katie Truong": """Name: Katie Truong
                    DOB: 31/12/2010
                    Address: 29, Sherringham Avenue, London N17 9RS
                    Mom: Mai Nguyen
                    07462111444
                    ngocmai76@yahoo.com""",
    "Oskar Tustain": """Name: Oskar Tustain
                    DOB: 3/11/2010
                    Address: 59, Uplands Road, London N8 9NH
                    Dad: Rob Tustain
                    07956250908
                    rob_tustain@hotmail.com""",
    "Daviya Watson": """Name: Daviya Watson
                    DOB: 1/7/2011
                    Address: Flat 2-3, 180, Wightman Road, London N8 0BT
                    Mom: Nordia Tucker
                    07412316631
                    nordsedwards@gmail.com""",
    "Sharnanita Winifred Opoku": """Name: Sharnanita Winifred Opoku
                    DOB: 26/4/2011
                    Address: 37, Argyle Road, London N17 0BE
                    Mom: Salomey Tawiah
                    07803425513
                    sazbio@hotmail.co.uk""",

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
    await update.message.reply_text("Welcome to information bot, please enter full name of the person：")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.message.text.strip()
    data = load_data()

    if user_id not in data:
        data[user_id] = {"used_free": True, "remaining": 0}
        reply = PERSON_DATA.get(name, f"『{name}』not found.Please contact t.me/iam_human333")
        await update.message.reply_text(f"【First time looking up is free】{reply}")
        save_data(data)
        return

    if data[user_id].get("remaining", 0) > 0:
        data[user_id]["remaining"] -= 1
        reply = PERSON_DATA.get(name, f"『{name}』not found.Please contact http://t.me/iam_human333")
        await update.message.reply_text(f"{reply}💎 {data[user_id]['remaining']} chances left")
        save_data(data)
    else:
        keyboard = [
            [InlineKeyboardButton("Contact to pay", url="https://t.me/iam_human333")]
        ]
        text = (
            """📌 You used up all chances.
                💷 packs avaliable
                1️⃣ time looking up：£2
                2️⃣ times looking up：£3
                5️⃣ times looking up：£8
                🆓 season VIP：£49
                Please click the button below to top-up 👇"""
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
        await update.message.reply_text(f"✅ added to {user_id} {count} times looking up")
    except (IndexError, ValueError):
        await update.message.reply_text("/add userID times")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    remaining = data.get(user_id, {}).get("remaining", 0)
    await update.message.reply_text(f"🔎 Your chances left：{remaining}")

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your user ID is：{update.effective_user.id}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("id", my_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
