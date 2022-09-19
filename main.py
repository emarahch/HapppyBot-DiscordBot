import os
import discord
import json
from discord.ext import commands
import re
import requests

my_secret = os.environ['TOKEN']
FA = os.environ['FACT']
RA = os.environ['Rapid']

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('We have logged in')


@bot.event
async def on_message(msg):
    msgL = msg.content.lower()
    mentalL = ['suicide', 'depressed', 'anxious']
    if any(x in msgL for x in mentalL):
        print('Keyword found')
        # embed = discord.Embed()
        embed = discord.Embed(
            title="Mental Health Resources ♡",
            description=
            "If you need help! [here](https://www.helpguide.org/find-help.htm).",
            color=discord.Color.from_rgb(255, 192, 203))
        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/3468/3468377.png")
        channel = msg.channel
        await channel.send(embed=embed)
    # fixes problem where commands wont work after on_message
    await bot.process_commands(msg)


@bot.command()
async def hello(ctx):
    print("worked")
    await ctx.send("Hey " + ctx.author.name + "!")


@bot.command()
async def meow(ctx):
    print("worked")
    await ctx.send("meow?")


@bot.command()
async def commands(ctx):
  print("worked")
  # await ctx.send("Hello, my commands are: \n !hello \n!meow \n!help \n!fact \n!horo \n!trivia")
  text = " \n !hello \n!meow \n!commands \n!fact \n!horo \n!trivia"
  embed = discord.Embed(title="Hello! My commands are... ♡", description=text,color=discord.Color.from_rgb(255, 192, 203))
  embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1391/1391308.png")
  await ctx.send(embed=embed)


@bot.command()
async def fact(ctx):
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': FA})
    if response.status_code == requests.codes.ok:
        txt = response.text
        print(txt)

        # await ctx.send(txt)

        embed = discord.Embed(title="Fact ♡",
                              description=txt,
                              color=discord.Color.from_rgb(255, 192, 203))
        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/8437/8437909.png")
        await ctx.send(embed=embed)
    else:
        print("Error:", response.status_code, response.text)
        return


# images used:
#https://www.flaticon.com/free-icon/cat_3468377     cat one


@bot.command()
async def horo(ctx):
    react = await ctx.send("What is your zodiac sign? ")
    zodiac = ['♏', '♐', '♑', '♒', '♓', '♈', '♉', '♊', '♋', '♌', '♍', '♎']
    for x in zodiac:
        await react.add_reaction(x)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in zodiac

    # [one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve]

    reaction, user = await bot.wait_for('reaction_add',
                                        check=check,
                                        timeout=30)

    if str(reaction.emoji) == '♏':
        sign = "scorpio"
    elif str(reaction.emoji) == '♐':
        sign = "sagittarius"
    elif str(reaction.emoji) == '♑':
        sign = "capricorn"
    elif str(reaction.emoji) == '♒':
        sign = "aquarius"
    elif str(reaction.emoji) == '♓':
        sign = "pisces"
    elif str(reaction.emoji) == '♈':
        sign = "aries"
    elif str(reaction.emoji) == '♉':
        sign = "Taurus"
    elif str(reaction.emoji) == '♊':
        sign = "gemini"
    elif str(reaction.emoji) == '♋':
        sign = "cancer"
    elif str(reaction.emoji) == '♌':
        sign = "leo"
    elif str(reaction.emoji) == '♍':
        sign = "virgo"
    elif str(reaction.emoji) == '♎':
        sign = "libra"

    url = "https://astro-daily-live-horoscope.p.rapidapi.com/horoscope-monthly/" + sign

    headers = {
        "X-RapidAPI-Key":RA,
        "X-RapidAPI-Host": "astro-daily-live-horoscope.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)
    txt = response.text
    embed = discord.Embed(title="Horoscope ♡",
                          description=txt,
                          color=discord.Color.from_rgb(255, 192, 203))
    embed.set_thumbnail(
        url="https://cdn-icons-png.flaticon.com/512/3013/3013224.png")
    await ctx.send(embed=embed)


@bot.command()
async def trivia(ctx):

    url = "https://opentdb.com/api.php?amount=1&type=boolean"
    response = requests.request("GET", url)
    data = json.loads(response.text)

    #initialize your list
    questionsL = []
    answersL = []

    # init dictionary - used only for testing
    myDic = {}

    for q in data['results']:
        questions = q['question']
        questionsL.append(questions)

    for a in data['results']:
        answers = a['correct_answer']
        answersL.append(answers)


# Used only fpr testing
    myDic = {questionsL[i]: answersL[i] for i in range(len(questionsL))}
    print(myDic)

    # actually used
    embed = discord.Embed(title="Trivia Game -True or False ♡",
                          description=questionsL[0],
                          color=discord.Color.from_rgb(255, 192, 203))
    embed.set_thumbnail(
        url="https://cdn-icons-png.flaticon.com/512/7967/7967969.png")
    await ctx.send(embed=embed)

    # response=await ctx.send(questionsL[0])

    def check(m):
        return m.content

    m = await bot.wait_for('message', check=check, timeout=30)

    if m.content == answersL[0]:
        print("wooohooo")
        embed = discord.Embed(title="Trivia Game -True or False ♡",
                              description="YOU GOT IT!",
                              color=discord.Color.from_rgb(255, 192, 203))
        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/7967/7967969.png")
        await ctx.send(embed=embed)
    else:
        print("noooo")
        print(answersL[0])
        embed = discord.Embed(title="Trivia Game -True or False ♡",
                              description="YOU FAILED :   (",
                              color=discord.Color.from_rgb(255, 192, 203))
        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/7967/7967969.png")
        await ctx.send(embed=embed)

bot.run(my_secret)

# https://www.flaticon.com/free-icon/black-cat_8490384?term=cat&page=1&position=93&page=1&position=93&related_id=8490384&origin=search

# https://www.flaticon.com/free-icon/parchment_3013224?term=astrology&page=1&position=16&page=1&position=16&related_id=3013224&origin=search

# https://www.flaticon.com/free-sticker/proud_8437909?related_id=8437909

# https://www.flaticon.com/free-icon/test_7967969?term=trivia&page=1&position=53&page=1&position=53&related_id=7967969&origin=search
# https://www.flaticon.com/free-icon/stars_1391308?term=cute&page=1&position=42&page=1&position=42&related_id=1391308&origin=search