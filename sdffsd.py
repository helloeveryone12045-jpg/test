import discord
from discord.ext import commands
import requests
import os
from flask import Flask
from threading import Thread

API_KEY = os.getenv("TRELLO_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
CARD_ID = os.getenv("CARD_ID")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")

app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def set_trello_status(status):
    url = f"https://api.trello.com/1/cards/{CARD_ID}"
    query = {
        'key': API_KEY,
        'token': TOKEN,
        'name': status
    }
    response = requests.request("PUT", url, params=query)
    return response.status_code == 200

def get_trello_status():
    url = f"https://api.trello.com/1/cards/{CARD_ID}"
    query = {
        'key': API_KEY,
        'token': TOKEN
    }
    response = requests.request("GET", url, params=query)
    if response.status_code == 200:
        return response.json().get('name')
    return None

@bot.command(aliases=['잠그기', '잠궈라', '섭닫', '봉인', '서버봉인', 'HC하케귀여움'])
@commands.has_permissions(administrator=True)
async def 잠금(ctx):
    if set_trello_status("LOCKED"):
        await ctx.send("🚨 **로블록스 서버가 봉쇄되었습니다.** 모든 플레이어가 추방됩니다.")
    else:
        await ctx.send("❌ 트렐로 연결에 실패했습니다.")

@bot.command(aliases=['해제', '풀어라', '열기', '봉인해제', '솔바람귀여움'])
@commands.has_permissions(administrator=True)
async def 오픈(ctx):
    if set_trello_status("UNLOCKED"):
        await ctx.send("🔓 **로블록스 서버 봉쇄가 해제되었습니다.** 이제 입장이 가능합니다.")
    else:
        await ctx.send("❌ 트렐로 연결에 실패했습니다.")

@bot.command()
async def 서버상태(ctx):
    status = get_trello_status()
    if status == "LOCKED":
        await ctx.send("현재 서버 상태: 🚨 **봉쇄됨 (LOCKED)**")
    elif status == "UNLOCKED":
        await ctx.send("현재 서버 상태: 🔓 **개방됨 (UNLOCKED)**")
    else:
        await ctx.send("❌ 서버 상태를 불러올 수 없습니다.")

keep_alive()
bot.run(DISCORD_BOT_TOKEN)
