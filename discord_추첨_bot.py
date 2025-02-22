import discord
import random
import csv
import os
from discord.ext import commands

# 봇 설정
intents = discord.Intents.default()
intents.messages = True           # 메시지 읽기
intents.guilds = True             # 서버 정보 접근
intents.members = True            # 서버 멤버 정보 접근
intents.message_content = True    # ✅ 메시지 내용 읽기 (필수)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is ready: {bot.user}')

# CSV 파일에서 사용자 이름과 지갑 주소 읽어오기
def read_participants_from_csv(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        participants = [(row['username'], row['wallet']) for row in reader if row.get('username') and row.get('wallet')]
    return participants

@bot.command()
async def draw(ctx, num_winners: int):
    """로컬 폴더에 있는 CSV 파일을 사용하여 무작위로 당첨자 선정"""
    try:
        file_path = "/Users/ijongseung/pnlc/discord_bot/list.csv"  # 폴더에 있는 파일 사용
        participants = read_participants_from_csv(file_path)

        if participants is None:
            await ctx.send("⚠️ No CSV file found in the folder.")
            return
        if not participants:
            await ctx.send("⚠️ No valid participants in the CSV file.")
            return
        if num_winners > len(participants):
            await ctx.send("⚠️ Number of winners exceeds the number of participants.")
            return

        winners = random.sample(participants, num_winners)
        result = "\n".join([f"🎉 **{username}** - {wallet}" for username, wallet in winners])
        await ctx.send(f"🎁 **Winner List:**🎁\n{result}\n ")

    except Exception as e:
        await ctx.send(f"⚠️ Error occurred: {str(e)}")
        
# 봇 실행 (Run the bot)
bot.run('')
