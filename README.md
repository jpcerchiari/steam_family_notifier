# 🎮 Steam Family Game Notifier

This application monitors Steam family libraries and automatically sends notifications to a Discord channel whenever new games are added.
Notifications include game cover, description, developer, release date, and direct Steam links.


---

# 📥 Clone the repository

```
git clone https://github.com/jpcerchiari/steam_family_notifier.git
cd steam_family_notifier
```

---

# 📦 Install dependencies

Before running the application, install the required Python packages:

`pip install -r requirements.txt`

This will install:

requests – for Steam API requests

discord.py – for sending notifications to Discord

python-dotenv – for reading environment variables from .env



---

# ⚙️ Configuration

Instead of manually creating a .env file, this project provides an interactive helper script:

`python config_env.py`

This will open a graphical interface where you can fill in the required fields. After confirmation, the script automatically generates a .env file in the project root.

The .env file contains the following variables:

- API_KEY: your Steam Web API key

- DISCORD_TOKEN: your Discord bot token

- DISCORD_CHANNEL_ID: the channel ID where notifications will be sent

- STEAM_IDS: JSON with family member names and their Steam64 IDs. To find your SteamID64, use [steamid.io](https://steamid.io)

- GAMES_FILE: filename where previously detected games are stored (must end with .json)

- LANGUAGE: language code for Steam game data (see [Steam Localization Languages](https://partner.steamgames.com/doc/store/localization))



---

# ▶️ Run the application

`python notificar_jogos_discord.py`

On the first run, the script only saves the current game list and does not send notifications.
From the second run onwards, it detects new games and sends alerts to Discord.


---

# ⏰ Automating execution

You can schedule the script to run automatically at regular intervals.

## 🐧 Linux (cron job)

1. Find the Python and script paths:
```
which python3
pwd
```

2. Open the crontab:

`crontab -e`


3. Add a job, for example to run every 6 hours:
```
0 */6 * * * /usr/bin/python3 /path/to/notificar_jogos_discord.py
```



---

## 🪟 Windows (Startup folder)

1. Press Win + R, type:

`shell:startup`


2. Create a shortcut pointing to your script or to a .bat file. Example .bat:


```
@echo off
cd C:\path\to\steam_family_notifier
python notificar_jogos_discord.py
```
This will run automatically when Windows starts.
