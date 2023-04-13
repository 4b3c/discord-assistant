import os, discord, subprocess, json, saveScript, instaloader, publishAWS, time
from PIL import ImageGrab
from io import BytesIO
from datetime import datetime
from itertools import dropwhile, takewhile
from instaloader import Post

saveScript.rewrite_json_file()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
path = "C://whySpace//discord-assistant//"
toggle_command = "hotspot.bat"
fav_folders = ["C://Users//Abram P//Desktop",
				"C://Users//Abram P//Downloads",
				"C://whySpace//discord-assistant"
			  ]


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

async def directory(message, folder, start):
	await message.channel.send('Here is a list of folders and files in ' + folder)
	for count in range(start, start + 10):
		try:
			await message.channel.send(os.listdir(folder)[count])
		except:
			break
	if (count + 1) % 10 == 0:
		await message.channel.send('[More]')
	else:
		await message.channel.send('[Done]')
	print(count)

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	await client.get_channel(1055600831442997351).send("I'm online!")

@client.event
async def on_message(message):
	if message.author.id != 599463127763124234:
		return

	print("A message was sent.")

	if message.content.startswith('toggle hotspot'):
		await message.channel.send('Toggling hotspot...')
		out = subprocess.check_output(toggle_command, shell=True)
		print("\n\nstart===>", out, "<===end\n\n")
		if out[4] == 10:
			out = "On"
		else:
			out = "Off"
		await message.channel.send('Mobile hotspot is now: ' + out)

	elif message.content.startswith('add command'):
		await message.channel.send('Adding command...')
		saveScript.rewrite_json_file()
		commContent = saveScript.replace_with_tabs(message.content)
		commContent = commContent.replace('	', '\t')
		with open('content.json', 'r') as f:
			current_content = json.load(f)
			f.close()
		current_content.append(current_content[-1])
		current_content[-2] = commContent
		with open('content.json', 'w') as f:
			json.dump(current_content, f, indent=3)
			f.close()

		await message.channel.send('Command Added...')
		saveScript.rewrite_py_file()
		subprocess.Popen(["python", path + "retrigger.py"], shell=True)
		await message.channel.send('Restarting...')
		print("\n\nStarted retrigger.py\n\n")
		await client.close()
		exit()

	elif message.content.startswith('help'):
		commands = ""
		for command in saveScript.get_commands():
			commands = commands + "\n- " + command
		await message.channel.send("Hi, here are all available commands :)\n" + commands)

	elif message.content.startswith('restart'):
		saveScript.rewrite_json_file()
		saveScript.rewrite_py_file()
		subprocess.Popen(["python", path + "retrigger.py"], shell=True)
		await message.channel.send("Restarting...")
		await client.close()
		exit()

	elif message.content.startswith('add import'):
		import_val = message.content.replace('add import ', 'import ') + ','
		with open('content.json', 'r') as f:
			content = json.load(f)
			f.close()
		content[0] = content[0].replace('import', import_val)
		with open('content.json', 'w') as f:
			json.dump(content, f)
			f.close()
		await message.channel.send('Added import :)')
		saveScript.rewrite_py_file()
		subprocess.Popen(["python", path + "retrigger.py"], shell=True)
		await message.channel.send("Restarting...")
		await client.close()
		exit()

	elif message.content.startswith('open app'):
		if "spotify" in message.content:
			os.system('spotify.exe')
			await message.channel.send('Opened spotify :)')

	elif message.content.startswith('take a screenshot'):
		screenshot = ImageGrab.grab(all_screens=True)
		screenshot.save('image.png')
		await message.channel.send(file=discord.File(fp='image.png'))

	elif message.content.startswith('send a file'):
		path = message.content.replace('send a file ', '')
		await message.channel.send(file=discord.File(fp=path))

	elif message.content.startswith('download instagram video'):
		link = message.content.replace('download instagram video ', '')
		shortcode = link.replace('https://www.instagram.com/reel/', '')
		i = 0
		while shortcode[i] != '/':
			i += 1
		shortcode = shortcode[0:i]

		L = instaloader.Instaloader()
		post = Post.from_shortcode(L.context, shortcode)
		L.download_post(post, target = 'instaVideos')
		for file in os.listdir('instaVideos'):
			if file[-3:-1] == 'mp':
				await message.channel.send(file=discord.File(fp=os.path.join('instaVideos',file)))

		for file in os.listdir('instaVideos'):
			os.remove(os.path.join('instaVideos', file))

		await message.channel.send('Cleared directory')

	elif message.content.startswith('send to esp'):
		ESPmessage = message.content.replace('send to esp ', '')
		if len(ESPmessage) > 54:
			await message.channel.send("Message too long :/")
			await message.channel.send("Remove atleast " + str(len(ESPmessage) - 54) + " characters")
		else:
			timeRN = time.strftime('%H:%M:%S')
			hour = int(timeRN[0:timeRN.index(":")])
			if hour > 12:
				timeRN = timeRN.replace(str(hour), str(hour - 12))
			elif hour == 0:
				timeRN = timeRN.replace("00", "12")
			publishAWS.send_esp_message(ESPmessage + "|" + timeRN)
			await message.channel.send("Sent your message to AWS MQTT :)")
			await message.channel.send(timeRN)

	elif message.content.startswith('show directory'):
		if message.content == "show directory":
			await message.channel.send("Here's a list of your favorites:")
			for fav in fav_folders:
				await message.channel.send(fav)
		else:
			folder = message.content.replace('show directory ', '')
			write_txt_file("last_folder.txt", folder)
			await directory(message, folder, 0)
		write_txt_file("set_10.txt", "0")

	elif message.content.startswith('open'):
		parent = await message.channel.fetch_message(message.reference.message_id)
		if parent.content.startswith("C://"):
			write_txt_file("last_folder.txt", parent.content)
			await directory(message, parent.content, 0)
			write_txt_file("set_10.txt", "0")
		elif parent.content.startswith("[More]"):
			last_folder = read_txt_file("last_folder.txt")
			set_10 = int(read_txt_file("set_10.txt")) + 1
			await directory(message, last_folder, 10 * set_10)
			write_txt_file("set_10.txt", str(set_10))
		else:
			last_folder = read_txt_file("last_folder.txt")
			last_folder = last_folder + "//" + parent.content
			await directory(message, last_folder, 0)
			write_txt_file("last_folder.txt", last_folder)
			write_txt_file("set_10.txt", "0")
		
		


client.run(token)