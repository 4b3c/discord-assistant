count = 10

print("Yo, run:" + str(count))
path = "C:/whySpace/ouroboros.py"

with open(path, "r") as f:
	content = f.read()
	f.close()

with open(path, "w") as f:
	if count > 10:
		content = content.replace("count = " + str(count), "count = " + str(count - 1))
		f.write(content)
		f.close()
		import subprocess
		subprocess.Popen("python " + path, shell=True)
	else:
		f.write(content)
		f.close()
