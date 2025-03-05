# This example requires the 'message_content' intent.

import discord
import json
import random
from discord import ui
from discord import app_commands
from discord.ext.commands import CheckFailure
from discord.ext import commands
import uuid

MY_GUILD = discord.Object(id=248864051092914177)  # replace with your guild id


class Blarry(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.commands = commands

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True
client = Blarry(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?berry'):
        await message.channel.send(get_blueberry())

def get_blueberry():
    with open('images.json') as images:
        images = json.load(images)
        image = random.choice(images)
        return image

@client.tree.command()
@app_commands.checks.has_role(878211597741490177)
@app_commands.describe(
    url='URL of an Image'
)
async def gib_more_berries(interaction: discord.Interaction, url: str):
    print(f'New Image added:{url}')
    image_list = []
    select = ui.Select(options=[discord.SelectOption(label='P&B')])
    view = ui.View()
    view.add_item(select)
    embed = discord.Embed(title='P&B')
    embed.add_field(name='Bla',value='blub')
    await interaction.user.send(view=view)
    with open('images.json') as images:
        image_list = json.load(images)
    image_list.append(url)
    with open("images.json", "w") as outfile:
        outfile.write(json.dumps(image_list, indent=4))
    await interaction.response.send_message(url)

@gib_more_berries.error
async def gib_more_berries_error(interaction: discord.Interaction, error):
    await interaction.response.send_message('You are not blue enough to do this')


@client.tree.command()
@app_commands.checks.has_role(878211597741490177)
async def show_all_berries(interaction: discord.Interaction):
    with open('images.json') as images:
        image_list = json.load(images)
        text=''
        for i in image_list:
            if len(text+i) > 2000:
                await interaction.channel.send(text)
                text = ''
            text = text + f'{i}\n'
        await interaction.channel.send(text)
        interaction.response.is_done()

@show_all_berries.error
async def gib_more_berries_error(interaction: discord.Interaction, error):
    await interaction.response.send_message('You are not blue enough to do this')



client.run('TOKEN')


# Add point system for berry sticker