import zipfile

z = zipfile.ZipFile(open("package.zip","wb"),mode="w")
z.writestr("shush_teams.py",open("shush_teams.py","rb").read())
