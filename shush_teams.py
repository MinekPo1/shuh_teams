import time
import subprocess
import sys
import requests


def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
	from pycaw.pycaw import AudioUtilities, AudioSession
except ImportError:
	install("pycaw")
	from pycaw.pycaw import AudioUtilities, AudioSession

# check for updates
version = "v1"
r = requests.get("https://api.github.com/repos/MinekPo1/shush_teams/releases")
j = r.json()
if r.status_code != 200:
	print("[!] Error: Could not check for updates")
elif j[0]["tag_name"] != version:
	print("[!] Update available: {}".format(j[0]["tag_name"]))
	print("[!] Downloading update...")
	r = requests.get(j[0]["assets"][0]["browser_download_url"])
	if r.status_code != 200:
		print("[!] Error: Could not download update")
	else:
		with open(__file__, "wb") as f:
			f.write(r.content)
		print("[!] Update downloaded")
		print("[!] Restarting...")
		subprocess.Popen(["python3", "shush_teams.py"])
		sys.exit()


print("Running...\r",end="")
t = time.time()
d = 3
try:
	while True:
		sessions: list[AudioSession] = AudioUtilities.GetAllSessions()

		if time.time() - t > 1:
			t = time.time()
			d = (d + 1) % 4
			print("Running"+"."*(d)+"   ",end="\r")

		for i in sessions:
			if i.Process and i.Process.name() == "Teams.exe":
				vol = i.SimpleAudioVolume
				if vol.GetMasterVolume() == 1:
					vol.SetMasterVolume(.02, None)
					print("Shuh")
except KeyboardInterrupt:
	print("\n[!] Shutting down...")
	sys.exit()
