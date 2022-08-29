from datetime import date
from ssl import CHANNEL_BINDING_TYPES
from statistics import geometric_mean
import discord
from discord import Option
import os
from dotenv import load_dotenv
import asyncio
import time
import random
import re
intents = discord.Intents.default()
client = discord.Client()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = discord.Bot()
GUILD_IDS = [1011677256273367040]  # ← BOTのいるサーバーのIDを入れます


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")


wolfrole = []
wolf = []       #狼
fox = []        #狐
ctizen = []     #市民
members = []
memberID = []
mem = []
sisya = []
position = []
goei = ""
uranai = ""
syugeki = ""
saisyu = ""

@bot.slash_command(description="人狼ゲームを開始します", guild_ids=GUILD_IDS)
async def wolfgame(
    ctx: discord.ApplicationContext,
    roles: Option(str, required=False, description="役職を「,」で区切って、入力してね")
):
    global wolfrole
    global wolf
    global fox
    global ctizen
    global members
    global memberID
    global mem
    global position

    position = roles.split(",")
    random.shuffle(position)
    embed = discord.Embed(title = "人狼ゲーム")
    embed.add_field(name = "参加者")
    for i in range(len(members)):
        mem.append(members[i])
        wolfrole.append(position[i])
        embed.add_field(name = members[i])

        if position[i] == "人狼":
            wolf.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011679813725073459
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)

        elif position[i] == "狂人":
            ctizen.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011679983892168794
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)

        elif position[i] == "狂信者":
            ctizen.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011698108524150844
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)
      
        elif position[i] == "狐":
            fox.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011680165396480090
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)

        
        elif position[i] == "占い師":
            ctizen.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011680090020646952
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)

        elif position[i] == "霊媒師":
            ctizen.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011680128851517591
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)
            

        elif position[i] == "騎士":
            ctizen.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011680060924760134
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)

        elif position[i] == "共有者":
            ctizen.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1011698174290825356
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)

        else:
            ctizen.append(members[i])
            user = ctx.guild.get_member(int(memberID[i]))
            role_id = 1013140055864397906
            role = ctx.guild.get_role(role_id)
            await user.add_roles(role)

    await ctx.send(embed=embed)
    await ctx.respond("役職を確認して勝利を目指しましょう")


@bot.slash_command(description="昼の行動を指示します", guild_ids=GUILD_IDS)
async def daytimeturn(
    ctx: discord.ApplicationContext
):
    global goei
    global uranai
    global syugeki
    global wolfrole
    global wolf
    global fox
    global ctizen
    global mem
    global sisya
    global position

    await ctx.send("昼がやってきました。")
    if (goei == syugeki):
        await ctx.send("昨夜の死亡者はいませんでした")
    if (uranai == "狐"):
        await ctx.send(str(uranai) + "が無残な姿で見つかりました")
        sisya.append(uranai)
        for i in range(len(mem)):
            if mem[i] == uranai:
                user = ctx.guild.get_member(int(memberID[i]))
                role_id = 1011698152761475092
                role = ctx.guild.get_role(role_id)
                await user.add_roles(role)

    if (syugeki != goei):
        await ctx.send(str(syugeki) + "が無残な姿で見つかりました")
        sisya.append(syugeki)
        for i in range(len(mem)):    
            if mem[i] == uranai:
                user = ctx.guild.get_member(int(memberID[i]))
                role_id = 1011698152761475092
                role = ctx.guild.get_role(role_id)
                await user.add_roles(role)

    else:
        await ctx.send("昨夜の死亡者はいませんでした")
    await ctx.respond("話し合い、それぞれの勝利を目指しましょう")


@bot.slash_command(description="昼の行動を指示します", guild_ids=GUILD_IDS)
async def daytime(
    ctx: discord.ApplicationContext,
    day: Option(str, required=False, description="議論時間を設定してください。デフォルトは２５０秒です")
):
    await ctx.respond("指定時刻になったらお知らせします")
    if not day:
        day = 250
    time.sleep(int(day))
    await ctx.send(str(day) + "秒経過しました。")
    await ctx.respond("生存者で多数決を取り、代表者１名が「/vote 追放したい方の名前{○○＃○○}」で追放してください")


@bot.slash_command(description="本日の追放者を指定してください", guild_ids=GUILD_IDS)
async def vote(
    ctx: discord.ApplicationContext,
    name: Option(str, required=False, description="追放者の名前{○○＃○○}")
):
    global sisya
    sisya.append(name)
    if not name:
        name = ctx.author
        for i in range(len(mem)):    
            if mem[i] == name:
                user = ctx.guild.get_member(int(memberID[i]))
                role_id = 1011698152761475092
                role = ctx.guild.get_role(role_id)
                await user.add_roles(role)
  
    await ctx.respond(str(name) + "が追放されました。夜の行動に移ってください。")


@bot.slash_command(description="夜の行動を指示します", guild_ids=GUILD_IDS)
async def nighturn(
    ctx: discord.ApplicationContext
):
    global goei
    global uranai
    global syugeki
    global wolfrole
    global wolf
    global fox
    global ctizen
    global mem
    global position

    await ctx.respond("夜がやってきました。全員就寝してください。チャットは禁止です")
    time.sleep(3)
    await ctx.send("騎士の方がいる場合は１名が２０秒以内に「/goeiturn 護衛したい方の名前{○○＃○○}」で行動してください")
    time.sleep(20)
    await ctx.send("占い師の方がいる場合は１名が２０秒以内に「/uranaiturn 占いたい方の名前{○○＃○○}」で行動してください")
    time.sleep(20)
    await ctx.send("人狼の方がいる場合は１名が２０秒以内に「/syugekiturn 襲撃したい方の名前{○○＃○○}」で行動してください")
    time.sleep(20)
    
    await ctx.respond("夜が明けました")
    

    
@bot.slash_command(description="ゲームが続くか判定します", guild_ids=GUILD_IDS)
async def gamecheck(
    ctx: discord.ApplicationContext
):
    global wolfrole
    global wolf
    global fox
    global ctizen
    global mem          #変更しない
    global position

    embed = discord.Embed(title = "試合終了")
    for i in range(len(position)):
        embed.add_field(name = mem[i], value = position[i])
    if (len(ctizen) == 0):
        if (len(fox) >= 1):
            await ctx.send(embed = embed)
            await ctx.respond("狐陣営の勝ちです！")
        elif ((len(wolf) >= 1) and (len(fox) == 0)):
            await ctx.send(embed = embed)
            await ctx.respond("人狼陣営の勝ちです！")
        else:
            await ctx.send("予期せぬエラーが起こりました")
    elif (len(wolf) == 0):
        if (len(fox) >= 1):
            await ctx.send(embed = embed)
            await ctx.respond("狐陣営の勝ちです！")            
        else:
            await ctx.send(embed = embed)
            ctx.respond("市民陣営の勝ちです！")
    else:
        await ctx.respond("試合はまだ続きます。それぞれの勝利を目指しましょう！")


@bot.slash_command(description="指定された人を護衛します", guild_ids=GUILD_IDS)
async def goeiturn(
    ctx: discord.ApplicationContext,
    name: Option(str, required=False, description="#nameを入力してね") 
):
    await ctx.send("護衛どちらか一人で、一回までにしてください")
    
    global goei
    goei = name
    await ctx.respond(str(goei) + "を護衛します")

@bot.slash_command(description="指定された人を占います", guild_ids=GUILD_IDS)
async def uranaiturn(
    ctx: discord.ApplicationContext,
    name: Option(str, required=False, description="#nameを入力してね")
):
    await ctx.send("占いはどちらか一人で、一回までにしてください")
    
    global uranai
    global mem          #変更しない
    global position

    uranai = name
    await ctx.send(str(uranai) + "を占います")
    
    for i in range(len(mem)):
        if(mem[i] == uranai):
            kekka = position[i]
        else:
            await ctx.send("予期せぬエラーが起きました")
    if (kekka == "人狼"):
        saisyu = "人狼です"
    elif (kekka == "狐"):
        saisyu = "人狼ではありません"
    else:
        saisyu = "人狼ではありません"       
    await ctx.respond(str(name) + "は" + str(saisyu))

@bot.slash_command(description="指定された人を襲撃します", guild_ids=GUILD_IDS)
async def syugekiturn(
    ctx: discord.ApplicationContext,
    name: Option(str, required=False, description="#nameを入力してね")
):
    await ctx.send("襲撃はどちらか一人で、一回までにしてください")
    
    global syugeki
    syugeki = name
    await ctx.respond(str(syugeki) + "を襲撃します")


@bot.slash_command(description="死亡者の役職を確認します", guild_ids=GUILD_IDS)
async def reibaiturn(
    ctx: discord.ApplicationContext,
    name: Option(str, required=False, description="#nameを入力してね") 
):
    global position
    global sisya
    for i in range(len(sisya)):
        if(sisya[i] == name):
            await ctx.respond(str(sisya) + "の役職は" + str(position[i]))
    await ctx.respond("以上です")



@bot.slash_command(description="役職一覧を開きます", guild_ids=GUILD_IDS)
async def wolfroles(
    ctx: discord.ApplicationContext
):
    global wolfrole
    embed = discord.Embed(title = "役職一覧")
    for i in range(len(wolfrole)):
        embed.add_field(name = wolfrole[i])
    await ctx.respond(embed=embed)
    

@bot.slash_command(description="参加者一覧を開きます", guild_ids=GUILD_IDS)
async def people(
    ctx: discord.ApplicationContext
):
    global members
    embed = discord.Embed(title = "参加者一覧")
    for i in range(len(members)):
        embed.add_field(name = members[i])
    await ctx.respond(embed = embed)


@bot.slash_command(description="参加者一覧を開きます", guild_ids=GUILD_IDS)
async def deadpeople(
    ctx: discord.ApplicationContext
):
    global sisya
    embed = discord.Embed(title = "参加者一覧")
    for i in range(len(sisya)):
        embed.add_field(name = sisya[i])
    await ctx.respond(embed = embed)

    

@bot.slash_command(description="ゲームを始める前に重労働", guild_ids=GUILD_IDS)
async def hello(
    ctx: discord.ApplicationContext
):
    global memberID
    global members
    members.append(ctx.author)
    memberID.append(ctx.author.id)
    await ctx.send(ctx.author)
    await ctx.respond(ctx.author.id)




bot.run(TOKEN)
client.run(TOKEN)
