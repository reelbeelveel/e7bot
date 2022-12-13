#!env/bin/python3

import sys
import os
import datetime
import json
import discord
import interactions
import requests
from dotenv import load_dotenv

bot = None
token = None

e7_url = "https://epic7x.com/character/"

def init_env():
    """Load the .env file and return the token"""
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        raise Exception("No token found in .env file")
    return token

def get_e7_character_data(character_name):
    """Get the data from the e7 website"""
    url = e7_url + character_name.lower().replace(" ", "-") + "/"
    print(url)
    r = requests.get(url)
    print(r.status_code)
    if r.status_code != 200:
        raise Exception("Error getting data from e7 website")
    return r.text, url

def parse_character_data(data, url, character_name):
    """Parse the data and return the character info"""
    lines = data.splitlines()

    # Get the image link -- Find line containing this string
    image_line = [line for line in lines if "var SELECTED_SKIN =" in line][0]
    image_link = image_line.split('=')[1]
    for _ in ["'", '"', ";"]:
        image_link = image_link.replace(_, "")
    image_link.strip()

    return interactions.Embed(
        title=f"{character_name.title()}",
        description=f"{character_name}",
        color=0xd700ff,
        timestamp=datetime.datetime.utcnow(),
        thumbnail=interactions.EmbedImageStruct(url=image_link),
        url=url
        #provider=interactions.EmbedProvider(name="Epic Seven Wiki", url="https://epic7x.com/")
    )

if __name__ == "__main__":
    token = init_env()
    bot = interactions.Client(token)

@bot.command(name="ping", description="Pong!")
async def ping(ctx: interactions.CommandContext):
    await ctx.send("Pong!")

@bot.command(
    name="get_character",
    description="Get the character info from the Epic Seven Wiki.",
    options = [
        interactions.Option(
            name="character",
            description="The Character to search for.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def get_character(ctx: interactions.CommandContext, character: str):
    try:
        character = character.lower()
        message = await ctx.send("Getting data...")
        data, url = get_e7_character_data(character)
        await message.edit(content=None, embeds=parse_character_data(data, url, character))
    except Exception as e:
        await message.edit(f"Hmmm... Something went wrong: {e}")


if __name__ == "__main__":
    bot.start()