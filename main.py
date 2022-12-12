#!env/bin/python3

import sys
import os
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

def get_e7_data(character_name):
    """Get the data from the e7 website"""
    url = e7_url + character_name.lower().replace(" ", "-") + "/"
    print(url)
    r = requests.get(url)
    print(r.status_code)
    if r.status_code != 200:
        raise Exception("Error getting data from e7 website")
    return r.text


if __name__ == "__main__":
    token = init_env()
    bot = interactions.Client(token)

@bot.command(name="ping", description="Pong!")
async def ping(ctx: interactions.CommandContext):
    await ctx.send("Pong!")

@bot.command(
    name="test",
    description="Test command",
    options = [
        interactions.Option(
            name="character",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def test(ctx: interactions.CommandContext, character: str):
    try:
        data = get_e7_data(character)
        await ctx.send(f"Done! {character}")
    except Exception as e:
        await ctx.send(f"Hmmm... Something went wrong: {e}")


if __name__ == "__main__":
    bot.start()
    


