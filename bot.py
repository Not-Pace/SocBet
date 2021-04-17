import os
import discord
from dbconnect import db
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

db1 = db()

bot = commands.Bot(command_prefix='sb.')

@bot.command(name='hi', help='It doesnt')
async def hello(ctx):
    response = 'Hello'
    await ctx.send(response)
    await ctx.message.add_reaction(":python3:736715611492581429")


@bot.command(name='ty', help='It doesnt')
async def danke(ctx):
    response = 'You\'re welcome'
    await ctx.send(response)

@bot.command(name='start', help="Initializes your user in the DB and gives you coins to start playing with!")
async def init_user(ctx):
    response = db1.init_user(ctx.message.author)
    await ctx.send(response)

@bot.command(name='nextup', help="Shows x number of next games (max x = 8)", aliases = ['nextmatches', 'nm', 'nextmatch'])
async def next_matches(ctx, num=1):
    if num>8:
        num=8
    results = db1.next_match(num)
    embed = discord.Embed(
        title = 'Next Matches',
        colour = discord.Colour.blue()
    )
    embed.set_thumbnail(url="https://i2.wp.com/www.samskoncept.com/wp-content/uploads/2020/04/EPL-LOGO.jpg?resize=1024%2C576&ssl=1")

    for i in range(num):
        match_details = results[i][0] + " vs " + results[i][1]
        match_starts = results[i][2].strftime("%b %d %Y %H:%M")
        match_odds = (results[i][4], results[i][6], results[i][5])
        embed.add_field(name = match_details, value = match_starts, inline= True)
        embed.add_field(name = "Odds in H:D:A", value = match_odds, inline= True)
        embed.add_field(name = '\u200b', value = '\u200b', inline= True)
    await ctx.send(embed = embed)
    await ctx.message.add_reaction(":python3:736715611492581429")

@bot.command(name='nextupfor', help="Shows x number of next games of team", aliases = ['nextmatchesfor', 'nmf'])
async def next_matches_team(ctx, name: str, num=1):
    if num>8:
        num=8
    results = db1.next_match_team(name, num)
    embed = discord.Embed(
        title = 'Next Match(es) for ' + name,
        colour = discord.Colour.blue()
    )
    embed.set_thumbnail(url="https://i2.wp.com/www.samskoncept.com/wp-content/uploads/2020/04/EPL-LOGO.jpg?resize=1024%2C576&ssl=1")
    if len(results) != 0:
        for i in range(num):
            match_details = results[i][0] + " vs " + results[i][1]
            match_starts = results[i][2].strftime("%b %d %Y %H:%M")
            match_odds = (results[i][4], results[i][6], results[i][5])
            embed.add_field(name = match_details, value = match_starts, inline= True)
            embed.add_field(name = "Odds in H:D:A", value = match_odds, inline= True)
            embed.add_field(name = '\u200b', value = '\u200b', inline= True)
    else:
        embed.add_field(name = "Are you", value = "dumb?")
    await ctx.send(embed = embed)
    await ctx.message.add_reaction(":python3:736715611492581429")

@bot.command(name='bet', help = 'specify the Home team and Away team and then specify H/D/A and then the amount of coins')
async def add_bet(ctx, home:str, away:str, side:str, amount:int):
    bet_stat = db1.add_bets(home, away, side, amount, ctx.message.author)
    if bet_stat:
        response = "Your bet has been placed!"
    else:
        response = "Details incorrect, please dont be dumb"
    await ctx.send(response)
    await ctx.message.add_reaction(":python3:736715611492581429")

@bot.command(name='showcoins', help = 'shows current amount of coins')
async def show_coins(ctx):
    response = "You have " + str(db1.show_coins(ctx.message.author)) + " coins, and have currently placed " + str(db1.show_bets(ctx.message.author)) + " bets"
    await ctx.send(response)
    await ctx.message.add_reaction(":python3:736715611492581429")

@bot.command(name='showbets', help = 'shows current bets')
async def show_current_bets(ctx):
    embed = discord.Embed(
        title = 'Current bets for ' + str(ctx.message.author),
        colour = discord.Colour.blue()
    )
    c_bets, fixtures = db1.show_current_bets(ctx.message.author)
    for i in range(len(c_bets)):
        match_name = fixtures[i][0][0] + " vs " + fixtures[i][0][1]
        deets = c_bets[i][2],c_bets[i][3], c_bets[i][5]
        embed.add_field(name = "Match Name", value = match_name, inline = True)
        embed.add_field(name = "Details", value = "Odds "+str(deets[0]) + "; Amount " + str(deets[1])+ "; Side " + str(deets[2]) + "; Potential winnings " + str(int(deets[0]*deets[1])), inline = True)
        embed.add_field(name = '\u200b', value = '\u200b', inline= False)
    await ctx.send(embed = embed)
    await ctx.message.add_reaction(":python3:736715611492581429")

bot.run(TOKEN)
