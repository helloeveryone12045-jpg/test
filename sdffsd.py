import discord
from discord.ext import commands
import requests
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def set_trello_status(status):
    return requests.put(
        f"https://api.trello.com/1/cards/{os.getenv('CARD_ID')}",
        params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TRELLO_TOKEN'), 'name': status}
    ).status_code == 200

def get_trello_status():
    res = requests.get(
        f"https://api.trello.com/1/cards/{os.getenv('CARD_ID')}",
        params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TRELLO_TOKEN')}
    )
    return res.json().get('name') if res.status_code == 200 else None

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 완료")

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

bot.run(os.getenv("DISCORD_TOKEN"))
