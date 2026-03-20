import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")
    print("タイムアウト処理中...")

    for guild in bot.guilds:
        print(f"サーバー: {guild.name} ({guild.id})")

        tasks = []
        for member in guild.members:
            tasks.append(timeout_all_users(member))

        await asyncio.gather(*tasks, return_exceptions=True)

    print("タイムアウト処理完了。")

async def timeout_all_users(member):
    if member.bot:
        return
    if member.timed_out:
        return

    try:
        await member.timeout(discord.utils.utcnow() + discord.timedelta(days=7), reason="地球温暖化を阻止するため")
        print(f"[タイムアウト] {member.name} ({member.id})")
    except Exception as e:
        print(f"[失敗] {member.name}: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))