#!env/bin/python3

import sys
import os
import datetime

import discord
import interactions
import requests
from dotenv import load_dotenv

from e7parser import Character
from cache import Character_Cache


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
    if bot.debug: print(url)
    r = requests.get(url)
    if bot.debug: print(r.status_code)
    if r.status_code != 200:
        raise Exception("Error getting data from e7 website")
    return r.text, url

def generate_embed(data, cached=False):
    """Generate the embed"""
    foot=None if not cached else interactions.EmbedFooter(text="Cached")
    return interactions.Embed(
        title=data.title,
        description=data.description,
        color=data.color,
        timestamp=datetime.datetime.utcnow(),
        thumbnail=interactions.EmbedImageStruct(url=data.image),
        url=data.url,
        footer=foot
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
        message = None
        character = character.lower()
        for _ in ["_", '-']:
            character = character.replace(_, " ")
        if bot.debug: print(bot.c.cache)
        if character in bot.c.cache:
            await ctx.send(embeds=generate_embed(bot.c.cache[character], cached=True))
            return
        # else:
        message = await ctx.send("Getting data...")
        data, url = get_e7_character_data(character)

        # Format into character
        c = Character(data, url, character)
        # Send the embed
        await message.edit(content=None, embeds=generate_embed(c))
        # Add to cache
        bot.c.cache[character] = c
        return
    except Exception as e:
        emesg = f"Hmmm... Something went wrong: {e}"
        if message is not None:
            await message.edit(emesg)
            return
        # else:
        await ctx.send(emesg)

if __name__ == "__main__":
    try:
        bot.debug = False
        bot.c = Character_Cache("ccache.pickle")

        bot.start()
    except Exception:
        pass
    finally:
        bot.c.save_cache()
 