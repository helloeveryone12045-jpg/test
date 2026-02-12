import discord
from discord.ext import commands
import requests
import os
API_KEY = os.getenv("TRELLO_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
CARD_ID = os.getenv("CARD_ID")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")

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

@bot.command()
@commands.has_permissions(administrator=True) # 관리자 권한 있는 사람만 가능
async def 잠금(ctx):
    if set_trello_status("LOCKED"):
        await ctx.send("🚨 **로블록스 서버가 봉쇄되었습니다.** 모든 플레이어가 추방됩니다.")
    else:
        await ctx.send("❌ 트렐로 연결에 실패했습니다.")

@bot.command()
@commands.has_permissions(administrator=True)
async def 해제(ctx):
    if set_trello_status("UNLOCKED"):
        await ctx.send("🔓 **로블록스 서버 봉쇄가 해제되었습니다.** 이제 입장이 가능합니다.")
    else:
        await ctx.send("❌ 트렐로 연결에 실패했습니다.")

@bot.command()
@commands.has_permissions(administrator=True)
async def 풀어라(ctx):
    if set_trello_status("UNLOCKED"):
        await ctx.send("🔓 **로블록스 서버 봉쇄가 해제되었습니다.** 이제 입장이 가능합니다.")
    else:
        await ctx.send("❌ 트렐로 연결에 실패했습니다.")

@bot.command()
@commands.has_permissions(administrator=True) # 관리자 권한 있는 사람만 가능
async def 잠궈라(ctx):
    if set_trello_status("LOCKED"):
        await ctx.send("🚨 **로블록스 서버가 봉쇄되었습니다.** 모든 플레이어가 추방됩니다.")
    else:
        await ctx.send("❌ 트렐로 연결에 실패했습니다.")
bot.run(DISCORD_BOT_TOKEN)
