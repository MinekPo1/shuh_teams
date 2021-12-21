# Shush_teams

This is a simple python script that automatically sets the volume of misbehaving apps to a lower volume in the mixer, if they try to set it high.

Originally written for teams, but can be used for any app.

## Installation

Requirements:

- **python**, written in python 3.9, however, it might work with earlier versions. If you are on windows you can install python 3.9 from the [Microsoft store](https://www.microsoft.com/store/productId/9P7QFQMJRFP7), if you are on Linux, I assume you know how to install python.

1. Click on the newest release and download the package.zip file.
2. Extract the contents, and run the shush_teams.py file.

## Settings

The script should generate a settings.yml file in the same directory as the script.

If you are not acquainted with yaml, you can read about it [here](https://www.yaml.org/start.html).

### mode

The mode setting can have one of the following values: `whitelist` or `blacklist`. The whitelist mode will only set the volume of apps whose names that match any regex in [match](#match) or include regex in [include](#include). The blacklist mode will do the opposite.

### match

This setting should be a list of regex expressions. If you don't know what regex is, just writhing the app executable name will most likely work.

### include

Similar to [match](#match), this setting should be a list of regex expressions, however here the expression does not have to match the whole name.

### trigger

Apps which pass the requirements outlined in [mode](#mode), will be checked if their volume is grater or equal to the value of this setting. If it is, the volume will be set to the value of [volume](#volume). If the [mute](#mute) setting is set to `true`, the app will be muted.

### volume

What the app's volume should be set to.

### mute

Whether apps should be muted or not.

### autoupdate

Whether the script should automatically update itself.
