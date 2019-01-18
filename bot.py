import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import random
import aiohttp
import os
import youtube_dl

Client = discord.Client
bot = commands.Bot(command_prefix="fw!")
bot.remove_command('help')

@bot.event
async def on_ready():
    print("this bot is ready to go and have a test run")
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    await loop()
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name = "W19")
    await bot.add_roles(member, role)

	
#------------------------------------------------------
#ids
julesjulicher2 = "266540652865519617"
lopendebank = "197062403400269824"
jannes = "455441990797230090"
axxel = "237654358500573184"
#____________________________________________

players = {}
queues = {}
def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


async def loop():
    while True:
        await bot.change_presence(game=discord.Game(name="prefix = fw!", type=2))
        await asyncio.sleep(5)
        await bot.change_presence(game=discord.Game(name="fijne f2p dagen", type=2))
        await asyncio.sleep(5)
        await bot.change_presence(game=discord.Game(name="welkom bij F2P W19", type=2))
        await asyncio.sleep(5)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(ctx, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title="Error:",
                              description="Damm it! I cant find that! Try `fw!help`.",
                              colour=0xff0000)
        await bot.send_message(error.message.channel, embed=embed)
    else:
        embed = discord.Embed(title="Error:",
                              description=f"{ctx}",
                              colour=0xff0000)
        await bot.send_message(error.message.channel, embed=embed)
    
#----------------------------------------------------------------------------------------------
#info cmds
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here is what i could find.", color=0xFF0000)
    embed.add_field(name="name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role, inline=True)
    embed.add_field(name="Joined at", value=user.joined_at, inline=True )
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(description="Here's what I could find:", color=0xff0000)
    embed.add_field(name="Name", value=ctx.message.server.name)
    embed.add_field(name="Owner", value=ctx.message.server.owner)
    embed.add_field(name="Region", value=ctx.message.server.region)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles))
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.add_field(name="Channels", value=len(ctx.message.server.channels))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)
#--------------------------------------------------------------------------------------------------
#overige cmds
@bot.command(pass_context=True)
async def ping(ctx):
        t1 = time.perf_counter()
        tmp = await bot.say("pinging...")
        t2 = time.perf_counter()
        await bot.say("Ping: {}ms".format(round((t2-t1)*1000)))
        await bot.delete_message(tmp)
@bot.command(pass_context=True)
async def changelog(ctx):
    await bot.say("bot is gemaakt")
@bot.command(pass_context=True)
async def setpfp(ctx, url):
    if ctx.message.author.id == julesjulicher2 or ctx.message.author.id == lopendebank:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.read()
            await bot.edit_profile(avatar=data)
            await bot.say("yep, als de profiel foto niet verandert, gebruik de cmd niet opnieuw maar wacht een uur en het zal gebeuren. dit heeft te maken met discord limits")    
        except:
            discord.errors.Forbidden
            
    else:
        await bot.say("nop")
#music cmds___________________________________________________
@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.say("ay okay :ok_hand:")
    await bot.join_voice_channel(channel)
    
@bot.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_bot = bot.voice_client_in(server)
    player = await voice_bot.create_ytdl_player(url, ytdl_options={'default_search': 'auto'}, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()
    await bot.say("your wish is my cmd")
	
@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_bot = bot.voice_client_in(server)
    await bot.say(":ok_hand: :dash:")
    await voice_bot.disconnect()

@bot.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await bot.say("muziek wordt gepauzeerd")

@bot.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await bot.say("muziek gaat verder")

@bot.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    await bot.say(":ok_hand: ay okay")
	
@bot.command(pass_context=True)
async def add(ctx, url):
    server = ctx.message.server
    voice_bot = bot.voice_client_in(server)
    player = await voice_bot.create_ytdl_player(url, ytdl_options={'default_search': 'auto'})
	
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await bot.say(":musical_note: video toegevoegd :musical_note:")

	
#_______________________________________
@bot.command(pass_context=True)
async def help(ctx):
    if ctx.message.author.id == julesjulicher2 or ctx.message.author.id == lopendebank or ctx.message.author.id == jannes or ctx.message.author.id == axxel:
        author = ctx.message.author
        embed = discord.Embed(colour = 0xff0000)
        embed.set_author(name="help")
        embed.add_field(name="serverinfo", value="geeft informatie over de server", inline = False)
        embed.add_field(name="info", value="geeft informatie over een persoon. gebruik dt!info @persoon", inline = False)
        embed.add_field(name="ping", value="x aantal ms vertraging", inline=False)
        embed.add_field(name="join", value="de bot joint de voice channel waar je in zit", inline=False)
        embed.add_field(name="leave", value="bot verlaat je voice channel", inline=False)
        embed.add_field(name="play", value="speelt een liedje van yt, gebruik play urlhere", inline=False)
        embed.add_field(name="pause", value="pauzeert het liedje", inline=False)
        embed.add_field(name="resume", value="liedje gaat verder", inline=False)
        embed.add_field(name="stop", value="stopt de muziek", inline=False)
        embed.add_field(name="changelog", value="geeft je een lijst van de laatste update", inline=False)
        #admin cmd
        embed.add_field(name="kick", value="kick de gementionde persoon **mod only**", inline=False)
        embed.add_field(name="reboot", value="precies wat het zegt, **dev only**", inline=False)
        embed.add_field(name="remove_cmd", value="verwijdert een cmd, **dev only**", inline=False)
        embed.add_field(name="sendm", value="gebruik = fw!sendm <channelidhere>")
        await bot.send_message(author, embed=embed)
    else:
        author = ctx.message.author
        embed = discord.Embed(colour = 0xff0000)
        embed.set_author(name="help")
        embed.add_field(name="serverinfo", value="geeft informatie over de server", inline = False)
        embed.add_field(name="info", value="geeft informatie over een persoon. gebruik dt!info @persoon", inline = False)
        embed.add_field(name="ping", value="x aantal ms vertraging", inline=False)
        embed.add_field(name="join", value="de bot joint de voice channel waar je in zit", inline=False)
        embed.add_field(name="leave", value="bot verlaat je voice channel", inline=False)
        embed.add_field(name="play", value="speelt een liedje van yt, gebruik play urlhere", inline=False)
        embed.add_field(name="pause", value="pauzeert het liedje", inline=False)
        embed.add_field(name="resume", value="liedje gaat verder", inline=False)
        embed.add_field(name="stop", value="stopt de muziek", inline=False)
        embed.add_field(name="changelog", value="geeft je een lijst van de laatste update", inline=False)
        await bot.send_message(author, embed=embed)
#----------------------------------------------------------------------------------------------------------------
#admin cmds
#----------------------------------------------------------------------------------------------------------------
@bot.command(pass_context = True)
async def kick(ctx, member: discord.Member):
	if ctx.message.author.id == julesjulicher2 or ctx.message.author.id == lopendebank or ctx.message.author.id == jannes or ctx.message.author.id == allex
        try:
            await bot.say(":boot: bye!""{}".format(member.mention))
            await bot.kick(member)
        except discord.errors.Forbidden:
            await bot.say(":x: error kan niet doen!, controleer of de bot boven de rang staat van de gene die je kickt")
    else:
        await bot.say("geen toegang")


@bot.command(pass_context=True)
async def reboot(ctx):
    if not (ctx.message.author.id == julesjulicher2 or ctx.message.author.id == lopendebank):
        return await bot.say(":x: geen toegang")
    await bot.say("ay okay :ok_hand:")
    await bot.logout()

@bot.command(pass_context=True)
async def remove_cmd(ctx, cmd):
    if not (ctx.message.author.id == julesjulicher2 or ctx.message.author.id == lopendebank):
        return await bot.say("No perms from developers")
    await bot.say("cmd is verwijdert :ok_hand:")
    bot.remove_command(cmd)
@bot.command()
async def sendm(ch, *, msg):
	if ctx.message.author.id == julesjulicher2 or ctx.message.author.id == lopendebank:
    	channel = bot.get_channel(ch)
    	if channel:
        	await bot.send_message(channel, msg)
    	else:
        	await bot.say('I can not find that channel')
	else:
		await bot.say("nene kun je lekker toch niet")





	
bot.run(os.environ.get('TOKEN'))
