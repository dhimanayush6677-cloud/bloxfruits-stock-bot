import discord
from discord.ext import tasks
import requests

import os
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1507319930524270714

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_stock = ""

def get_stock():
    url = "https://blox-fruits-stock-fruit-api.vercel.app/api/stock"

    try:
        response = requests.get(url)
        data = response.json()

        normal = "\n".join(data["normal"])
        mirage = "\n".join(data["mirage"])

        return f"""
🍏 **Blox Fruits Stock Update**

🟢 **Normal Dealer**
{normal}

🌙 **Mirage Dealer**
{mirage}
"""

    except Exception as e:
        return f"Error: {e}"

@tasks.loop(minutes=240)
async def stock_update():
    global last_stock

    channel = client.get_channel(CHANNEL_ID)
    stock = get_stock()

    if stock != last_stock:
        last_stock = stock
        await channel.send(stock)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    stock_update.start()

client.run(TOKEN)
