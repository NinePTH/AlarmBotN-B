import asyncio
import discord
from discord.ext import commands
from time import strftime
from dateutil import parser
from datetime import datetime
import os
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import random


alarmList2 = {}

bot = commands.Bot(command_prefix="A!", help_command = None)
client = discord.Client()

@bot.command()
async def help(ctx):
    emBed =  discord.Embed(title="Alarm bot", description = "คำสั่งทั้งหมดของบอทตัวนี้",color = 0x0356fc)
    emBed.add_field(name = "A!help", value = "รับการช่วยเหลือ", inline = False)
    emBed.add_field(name = "A!la", value = "ดูลิสท์นาฬิกาปลุก", inline = False)
    emBed.add_field(name = "A!alarm", value = "ตั้งนาฬิกาปลุก", inline = False)
    emBed.add_field(name = "A!a", value = "ตั้งนาฬิกาปลุก", inline = False)
    emBed.add_field(name = "A!d", value = "ลบนาฬิกาปลุก", inline = False)
    emBed.add_field(name = "A!rm", value = "ลบนาฬิกาปลุก", inline = False)
    emBed.add_field(name = "A!delete", value = "ลบนาฬิกาปลุก", inline = False)
    emBed.add_field(name = "A!remove", value = "ลบนาฬิกาปลุก", inline = False)
    emBed.add_field(name = "A!leave", value = "สั่งให้นาฬิกาปลุกออกจากห้องพูดคุย", inline = False)
    emBed.add_field(name = "A!logout", value = "สั่งให้บอทออกจากระบบ", inline = False)
    emBed.add_field(name = "A!play (url)", value = "สั่งให้เปิดเพลง", inline = False)
    emBed.add_field(name = "A!xo @ชื่อผู้เล่น 1 @ชื่อผู้เล่น 2", value = "เล่นเกมxo (2คน)", inline = False)
    emBed.add_field(name = "การตั้งเวลาปลุก", value = "ตัวอย่าง : >a 27-04-2023 00:01:00 หรือ 16:00 หรือ 12-24 10:00")
    emBed.set_thumbnail(url="https://www.seekpng.com/png/full/23-233625_alarm-clock-icon-alarm-clock-icon-png.png")
    emBed.set_footer(text="บอทสำหรับแจ้งเตือน", icon_url = "https://www.seekpng.com/png/full/23-233625_alarm-clock-icon-alarm-clock-icon-png.png")
    await ctx.channel.send(embed = emBed)

@bot.command()
async def logout(ctx):
    await bot.logout()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*20)
    await bot.change_presence(activity=discord.Game(name='สามารถดูคำสั่งต่างๆได้ด้วยการพิมพ์ A!help'))





@bot.command()  
async def time(ctx):
    time_str = strftime("%H:%M:%S")
    await ctx.send("```"+time_str+"```")
    del time_str


# END COMMANDS----------------------

# BEGIN ALIASES---------------------

@bot.command(pass_context=True)
async def la(ctx):
    await internal_alarmlist(ctx)


@bot.command(pass_context=True)
async def alarm(ctx,*, time):
    await internal_alarm(ctx, time)


@bot.command(pass_context=True)
async def a(ctx,*, in_time):
    await internal_alarm(ctx, in_time)


@bot.command(pass_context=True)
async def d(ctx, ind):
    await internal_remove_alarm(ctx, ind)


@bot.command(pass_context=True)
async def rm(ctx, ind):
    await internal_remove_alarm(ctx, ind)


@bot.command(pass_context=True)
async def delete(ctx, ind):
    await internal_remove_alarm(ctx, ind)


@bot.command(pass_context=True)
async def remove(ctx, ind):
    await internal_remove_alarm(ctx, ind)



async def internal_alarmlist(contx):  
    embed = discord.Embed(title=":alarm_clock:Alarm List", color=0x22a7cc)
    embed.set_thumbnail(url="https://www.seekpng.com/png/full/23-233625_alarm-clock-icon-alarm-clock-icon-png.png")
    print('Current alarm list:')
    if contx.channel not in alarmList2.keys() or alarmList2[contx.channel] == []:
        await contx.send('ยังไม่มีนาฬิกาปลุกที่ตั้งไว้ในช่องนี้. เพิ่มนาฬิกาปลุกด้วยการใช้คำสั่ง ' + "A!" + 'alarm [เวลา].')
        return
    for i in range(len(alarmList2[contx.channel])):
        embed.add_field(name='#' + str(i + 1) + ':' + str(alarmList2[contx.channel][i].name).split('#', 1)[0],
                        value=str(alarmList2[contx.channel][i].time), inline=True)
        print('#' + str(i + 1) + ':' + str(alarmList2[contx.channel][i].name) + " -> " + str(alarmList2[contx.channel][i].time))
    print('-'*50)
    await contx.send(embed=embed)


async def internal_alarm(contx, inp):  
    try:
        alarm_time = parser.parse(inp)
    except:
        await contx.send(":negative_squared_cross_mark:โปรดใช้รูปแบบนี้ \"[M-D-Y] H:M:S\".\
__ตัวอย่าง:__\
12-24 10:00 = วันที่24 ธันวาของปีนี้ เวลา 10:00:00. \
12:30 = 12:30 ของวันนี้.\
__ถ้าไม่ได้ใส่วันที่ ระบบจะกำหนดให้เป็นวันนี้.__")
        return
    if alarm_time < datetime.now():
        await contx.send('วันที่หรือเวลาที่คุณใส่มาผ่านมาแล้ว นาฬิกาปลุกจะไม่ถูกตั้ง')
        return

    temp = Alarm(contx.author, alarm_time)
    if contx.channel not in alarmList2.keys():
        alarmList2.update({contx.channel: []})

    alarmList2[contx.channel].append(temp) 
    del temp

    await contx.send(
        ":white_check_mark:" + ("นาฬิกาปลุกของ") + contx.author.mention + "ถูกเซทให้เป็น **" + str(alarm_time.date()) + ", " + str(
            alarm_time.time()) + "**!")


async def internal_remove_alarm(contx, index):
    index = int(index) - 1
    if contx.author == alarmList2[contx.channel][index].name:  
        alarm_time = alarmList2[contx.channel][index].time
        await contx.send(":white_check_mark:นาฬิกาปลุก ณ **" + str(alarm_time.date()) + ", "
                         + str(alarm_time.time()) + "** ถูกลบ.")
        del alarmList2[contx.channel][index]
        del alarm_time
    else:
        await contx.send("นาฬิกาปลุกที่คุณจะลบไม่ใช่ของคุณ.")



class Alarm:
    name = None
    time = None

    def __init__(self, usr, t):
        self.name = usr
        self.time = t



async def check_alarms():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for alarmList in alarmList2.values():
            for i in range(len(alarmList)):
                if alarmList[i].time < datetime.now():
                    await alarmList[i].name.create_dm()
                    await alarmList[i].name.dm_channel.send(content=":alarm_clock:Your alarm for **"+str(alarmList[i].time)+"** just rang!")
                    #print("alarm of "+str(alarmList[i].name)+" just rang!")
                    channel = alarmList[i].name.voice.channel
                    #if alarmList[i].name.voice in voice.channel:
                    await channel.connect()
                    ydl_opts = {'format': 'bestaudio'}
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info('https://www.youtube.com/watch?v=iNpXCzaWW1s%27', download=False)
                    URL = info['formats'][0]['url']
                    voice = get(bot.voice_clients, guild=alarmList[i].name.guild)
                    voice.play(discord.FFmpegPCMAudio(URL))
                    print("alarm of "+str(alarmList[i].name)+" just rang!")
                    alarmList.pop(i)
                    #elif alarmList[i].name.voice is None:
                    #    await alarmList[i].name.dm_channel.send("You're not in the voice channel")

                    #if alarmList[i].name.voice is None:
                    #    await alarmList[i].name.dm_channel.send("You're not in the voice channel")
                    #    channel = alarmList[i].name.voice.channel
                    #    alarmList.pop(i)
                    #    return
                    #else:
                    #    await channel.connect()
                    #    ydl_opts = {'format': 'bestaudio'}
                    #    with YoutubeDL(ydl_opts) as ydl:
                    #        info = ydl.extract_info('https://www.youtube.com/watch?v=iNpXCzaWW1s%27', download=False)
                    #    URL = info['formats'][0]['url']
                    #    voice = get(bot.voice_clients, guild=alarmList[i].name.guild)
                    #    voice.play(discord.FFmpegPCMAudio(URL))
                    #i got a bug in this function when alarm owner is not in anychannel bot will cracked
                    alarmList.pop(i)
        await asyncio.sleep(5)



#@bot.command()
#async def join(ctx):
#    channel = ctx.author.voice.channel
#    await channel.connect()

@bot.command()
async def play(ctx,url):
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None:
        ctx.channel.send("เข้า voice channel แล้ว")
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)

    YDL_OPTIONS = {"format" : "bestaudio", "noplaylist" : "True"}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice_client.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice_client.is_playing()
    else:
        await ctx.channel.send("เพลงถูกเล่นอยู่แล้ว")
        return

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


bot.loop.create_task(check_alarms())

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command()
async def xo(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("ตาของ <@" + str(player1.id)+">")
        elif num == 2:
            turn = player2
            await ctx.send("ตาของ <@" + str(player2.id)+">")
    else:
        await ctx.send("เกมกำลังเล่นอยู่ กรุณาเล่นให้จบก่อนจึงเริ่มเกมใหม่")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " ชนะ!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("เสมอ!")

                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("กรุณาเลือกเลข1-9")
        else:
            await ctx.send("ไม่ใช่ตาของคุณ")
    else:
        await ctx.send("สามารถเล่นใหม่ได้ด้วยการใช้คำสั่ง A!xo")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@xo.error
async def xo_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("กรุณาแท็กผู้ใช้2คนเพื่อเล่นเกมนี้")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("กรุณาตรวจสอบให้ดีว่าแท็กผู้ที่จะเล่นแล้ว (ตย. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("โปรดเลือกตำแหน่งที่คุณต้องการ")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("โปรดเช็คให้ดีว่าคุณใส่ตัวเลข")

bot.run('*token')
