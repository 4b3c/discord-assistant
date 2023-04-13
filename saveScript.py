import json


def rewrite_json_file():
	with open('discord_automator.py', 'r') as f:
		content = f.read()
		f.close()

	content = content.replace('    ', '\t')
	content = content.split("\tif message.content.startswith")
	content[1] = "\tif message.content.startswith" + content[1]

	content[1] = content[1].split("\telif message.content.startswith")
	for statement in range(len(content[1])):
		if statement == 0:
			content.append(content[1][0])
		else:
			content.append("\telif message.content.startswith" + content[1][statement])

	del content[1]
	content[-1] = content[-1].replace("\n\nclient.run(token)", "\n")
	content.append("\nclient.run(token)")
	
	with open('content.json', 'w') as f:
		json.dump(content, f, indent=3)
		f.close()


def rewrite_py_file():
	with open('content.json', 'r') as f:
		content = json.load(f)
		f.close()

	total_content = ''
	for section in content:
		total_content += section
		
	with open('discord_automator.py', 'w') as f:
		f.write(total_content)
		f.close()

def get_commands():
	with open('content.json', 'r') as f:
		current_content = json.load(f)
		f.close()

	commands = []
	for statement in range(len(current_content))[1:-1]:
		counter = 0
		command = ""
		print(statement)

		while current_content[statement][counter] != "'":
			counter += 1
		counter += 1
		print(current_content[statement][counter] + "HELLOOOOOOOO")

		while current_content[statement][counter] != "'":
			command += current_content[statement][counter]
			counter += 1
		commands.append(command)

	print(commands)
	return commands

def replace_with_tabs(string):
	return string.replace('add command\n', '').replace('    ', '\t') + "\n\n"


rewrite_json_file()