# Steamupdate.py

This script checks for steam dedicated server updates based on [LinuxGSM](https://linuxgsm.com/). It compares the build ID of the running server with the Steam build ID and then stop, backup, update and run the server. It also notifies the users through Discord Webhook (if the variable exists) 5mn before, 1mn before and then operates the update.

**WIP :** I'll use `docopt` in a future version to merge both `dailybackup.py` and `steamupdate.py` scripts into a single one.

## Requirements

### System

- Python >= 3.6
- steamcmd

### Python

- requests

## Environment variables

| Variable name | Description | Example | Required |
|---------------|-------------|---------|----------|
| APP_DIR | The directory where the Steam Dedicated Server is installed | `/home/user/valheim` | True |
| APP_EXECUTABLE | The executable launched to start/stop the server | `vhserver` | True |
| APP_ID | The Steam ID of the app | `896660` | True |
| DISCORD_WEBHOOK_URL | The Discord Webhook URL to send messages to | https://discord.com/api/webhooks/****************\/************************** | False |

## CRON examples

Backup the server everyday at 6AM:

```
0 6 * * * user APP_DIR=/home/user/valheim APP_EXECUTABLE=vhserver DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxxxx" python3.6 /home/user/dailybackup.py
```

Check every 10mn if a server update is available and then update it:

```
*/10 * * * * user APP_ID=896660 APP_DIR=/home/user/valheim APP_EXECUTABLE=vhserver DISCORD_WEBHOOK_URL="xxxxxxxxxx/xxxxxxxxxx" python3.6 /home/user/steamupdate.py
```
