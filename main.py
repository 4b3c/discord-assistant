import discord
from discord.ext import commands
import subprocess
from PIL import ImageGrab


intents = discord.Intents.all()
path = "C://whySpace//discord-assistant//"
channel_id = 1055600831442997351
hotspot_toggle_file = "hotspot.bat"

def read_txt_file(path):
	with open(path, "r") as f:
		content = f.read()
		f.close()
		return content

def write_txt_file(path, content):
	with open(path, "w") as f:
		f.write(content)
		f.close()

token = read_txt_file(path + "token_pass.txt")
bot = commands.Bot(command_prefix='!', intents=intents)





class Buttons(discord.ui.View):
	def __init__(self, *, timeout=180):
		super().__init__(timeout=timeout)

	@discord.ui.button(label="Button", style=discord.ButtonStyle.gray)
	async def gray_button(self, button:discord.ui.Button, interaction:discord.Interaction):
		await interaction.response.send('You clicked the button!')












@bot.event
async def on_ready():
	# print(f'Logged in as {bot.user.name}')
	await bot.get_channel(channel_id).send('I\'m online!')

@bot.command(brief="Say hello!")
async def hello(ctx):
	await ctx.send('Hello!')

@bot.command(brief="Check bot latency")
async def ping(ctx):
	latency = round(bot.latency * 1000)
	await ctx.send(f'Pong! Latency is {latency}ms')

@bot.command(brief="Turn off the bot")
async def terminate(ctx):
	await ctx.channel.send('Shutting down.')
	await bot.close()
	exit()

@bot.command(brief="Toggle the computer hotspot")
async def hotspot(ctx):
	await ctx.channel.send('Toggling hotspot...')
	out = subprocess.check_output(hotspot_toggle_file, shell=True)
	# print("\n\nstart===>", out, "<===end\n\n")
	if out[4] == 10: out = "On"
	else: out = "Off"
	await ctx.channel.send('Mobile hotspot is now: ' + out)

@bot.command(brief="Screenshot the computer screen")
async def screenshot(ctx):
	screenshot = ImageGrab.grab(all_screens=True)
	screenshot.save('image.png')
	await ctx.channel.send(file=discord.File(fp='image.png'))

@bot.command(brief="Test extended commands")
async def test(ctx):
	embed = discord.Embed(
		title="Test Command",
		description="This command is how I test new things.",
	)

	embed.set_author(name="Automator")
	embed.add_field(name="Python Code", value="```python\nprint('Hello, world!')\n```", inline=False)

	await ctx.send(embed=embed, view=Buttons())

	# view = discord.ui.View() # Establish an instance of the discord.ui.View class
	# style = discord.ButtonStyle.gray  # The button will be gray in color
	# item = discord.ui.Button(style=style, label="Read the docs!", url="https://discordpy.readthedocs.io/en/master")  # Create an item to pass into the view class.
	# view.add_item(item=item)  # Add that item into the view class
	# await ctx.send("This message has buttons!", view=view)  # Send your message with a button.
	


# Start the bot
bot.run(token)
