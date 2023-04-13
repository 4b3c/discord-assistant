import time, subprocess

path = "C:/whySpace/discord_bot/discord_automator.py"

time.sleep(5)
print("Starting")

subprocess.Popen(["python", path], shell=True)

print("Done")