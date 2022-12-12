#!/env/python3

import sys
import os
import json
import discord
import interactions
from dotenv import load_dotenv

bot = None
token = None

def init_env():
    """Load the .env file and return the token"""
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        raise Exception("No token found in .env file")
    return token



if __name__ == "__main__":
    token = init_env()
    bot = interactions.Client(token)

@bot.command(name="ping", description="Pong!")
async def ping(ctx: interactions.CommandContext):
    await ctx.send("Pong!")

if __name__ == "__main__":
    bot.start()
    


