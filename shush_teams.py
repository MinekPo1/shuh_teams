import io
import time
import sys
import requests
import zipfile
import yaml
import subprocess
import re


def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
	import jsonschema
except ImportError:
	install("jsonschema")
	import jsonschema
try:
	from pycaw.pycaw import AudioUtilities, AudioSession
except ImportError:
	install("pycaw")
	from pycaw.pycaw import AudioUtilities, AudioSession


SETTINGS_FILE_PATH = __file__.replace(
	__file__.split("/")[-1].split("\\")[-1], "settings.yml"
)

settings = {
		"volume": 0.02,
		"trigger":1,
		"mute": False,
		"mode": "whitelist",
		"match": [
			"Teams.exe",
		],
		"includes":[],
		"autoupdate": True,
	}

# check if file exists, and load it if yes
try:
	with open(SETTINGS_FILE_PATH, "r") as f:
		schema = {
			"$schema": "http://json-schema.org/draft-07/schema#",
			"type": "object",
			"properties": {
				"volume": {
					"type": "number",
					"minimum": 0,
					"maximum": 1,
				},
				"mute": {
					"type": "boolean",
				},
				"match": {
					"type": "array",
					"items": {
						"type": "string",
					},
				},
				"mode": {
					"type": "string",
					"enum": ["whitelist", "blacklist"],
				},
				"includes": {
					"type": "array",
					"items": {
						"type": "string",
					},
				},
				"trigger": {
					"type": "number",
					"minimum": 0,
					"maximum": 1,
				},
				"autoupdate": {
					"type": "boolean",
				}
			},
		}
		j = yaml.safe_load(f)

		try:
			jsonschema.validate(j, schema)
			settings.update(j)  # allow missing keys
		except jsonschema.ValidationError as e:
			print("[!] Error: Invalid settings file")
			print(e)
			print("[!] Using default settings")

except FileNotFoundError:
	print("[!] Settings file not found, creating...")
	with open(SETTINGS_FILE_PATH, "w") as f:
		yaml.safe_dump(settings, f)


# check for updates
if settings["autoupdate"]:
	version = "v1.5"
	r = requests.get("https://api.github.com/repos/MinekPo1/shuh_teams/releases")
	j = r.json()
	if r.status_code != 200:
		print("[!] Error: Could not check for updates")
	elif j[0]["tag_name"] > version:
		print("[!] Update available: {}".format(j[0]["tag_name"]))
		print("[!] Downloading update...")
		r = requests.get(j[0]["assets"][0]["browser_download_url"],stream=True)
		if r.status_code != 200:
			print("[!] Error: Could not download update")
		else:
			s = io.BytesIO()
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					s.write(chunk)
					print(
						"[!] Downloading: {}%".format(int(s.tell()/s.getbuffer().nbytes*100)),
						end="\r"
					)
			print("[!] Downloading: 100%")
			z = zipfile.ZipFile(s)
			for i in z.filelist:
				if i.filename == "shush_teams.py":
					d = z.read(i)
					with open(__file__, "wb") as f:
						f.write(d)
					print("[!] Update downloaded")
					print("[!] Restarting...")
					subprocess.Popen([sys.executable, __file__])
					sys.exit()
		print("[!] Update not downloaded")
else:
	print("[!] Autoupdate disabled")

print("Running...\r",end="")
t = time.time()
d = 3
try:
	p_app = None
	app_x = 0
	while True:
		sessions: list[AudioSession] = AudioUtilities.GetAllSessions()

		if time.time() - t > 1:
			t = time.time()
			d = (d + 1) % 4
			print("Running"+"."*(d)+"   ",end="\r")

		for i in sessions:
			if i.Process:
				matches = (
					any(
						re.fullmatch(j, i.Process.name()) is not None
						for j in settings["match"]
					)
					or any(
						re.search(j, i.Process.name()) is not None
						for j in settings["includes"]
					)
				)

				if not(matches ^ (settings["mode"] == "whitelist")):
					vol = i.SimpleAudioVolume
					if vol.GetMasterVolume() >= settings["trigger"]:
						vol.SetMasterVolume(settings["volume"], None)
						vol.SetMute(settings["mute"], None)
						if p_app != i.Process.name():
							print("Shush",i.Process.name())
							app_x = 1
							p_app = i.Process.name()
						else:
							app_x += 1
							print("\033[FShush",i.Process.name(),"x",app_x)
except KeyboardInterrupt:
	print("\n[!] Shutting down...")
	sys.exit()
