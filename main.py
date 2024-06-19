import discord
from discord.ext import commands
import json
import os
from datetime import datetime


intents = discord.Intents.all()
intents.members = True
intents.reactions = True  
bot = commands.Bot(command_prefix=".", intents=intents)


VERIFICATION_DATA_FILE = "verification_data.json"

def load_verification_data():
    if os.path.isfile(VERIFICATION_DATA_FILE):
        with open(VERIFICATION_DATA_FILE, "r") as file:
            return json.load(file)
    return {
        "verification_message_id": None,
        "verification_emoji_id": None,  
        "verification_role_id": 1247238261970047066
    }


def save_verification_data(data):
    with open(VERIFICATION_DATA_FILE, "w") as file:
        json.dump(data, file)


verification_data = load_verification_data()

bot.remove_command('help')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{round(error.retry_after, 2)} seconds cooldown")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Working"))
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("hey")

@bot.command()
@commands.has_permissions(administrator=True)
async def verify(ctx):
    global verification_data

    verification_data = {
        "verification_message_id": None,
        "verification_emoji_id": None,  
        "verification_role_id": 1247238261970047066
    }

    save_verification_data(verification_data)

    # Get the custom emoji object
    emoji2 = discord.utils.get(ctx.guild.emojis, name="emoji_102")
    emoji = discord.utils.get(ctx.guild.emojis, name="emoji_63")  # Replace with actual emoji name

    embed = discord.Embed(
        title="React below to get verified",
        description=f" {emoji2} . ݁₊ ⊹ . ݁˖ . ݁ welc♡",   
        color=discord.Color.from_rgb(252, 222, 255) 
    )


    file = discord.File("image.jpg", filename="image.jpg")
    embed.set_image(url="attachment://image.jpg")

    message = await ctx.send(embed=embed, file=file)
    await message.add_reaction(emoji)  


    verification_data["verification_message_id"] = message.id
    verification_data["verification_emoji_id"] = emoji.id
    save_verification_data(verification_data)




@bot.event
async def on_raw_reaction_add(payload):

    if (verification_data["verification_message_id"] is not None and
        payload.message_id == verification_data["verification_message_id"] and
        payload.emoji.id == verification_data["verification_emoji_id"]):  

        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(verification_data["verification_role_id"])
        member = guild.get_member(payload.user_id)

        if role and role not in member.roles:
            await member.add_roles(role)
            print(f"Added {role.name} to {member.name}")






bot.run('MTI1MTk5MzkxMTM5MjczNTQxNw.GGrVku.sQjQu5spc0QLmWC_eY1jL5NFHkZoY8bEhV606c')
