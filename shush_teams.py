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
version = (0,0,1)
requests.get("github.com/repos/MinekPo1/{repo}/releases")


print("Running...\r",end="")
t = time.time()
d = 3
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
