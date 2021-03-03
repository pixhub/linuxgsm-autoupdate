import os
import subprocess
import requests
import time
import sys
import datetime


def discord_message(message):
    if "DISCORD_WEBHOOK_URL" in os.environ:
        discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        message_timestamp = datetime.datetime.now().strftime("%H:%M:%S: ")
        data = {"content": message_timestamp + message}
        requests.post(discord_webhook_url, json=data)


def stop_server():
    try:
        subprocess.call([os.getenv('APP_DIR') + "/" + os.getenv('APP_EXECUTABLE'), "stop"])
        discord_message("Server successfuly Shutdown")

    except:
        discord_message("An error occured while stopping the server. Please contact your administrator")
        sys.exit(1)


def backup_server():
    try:
        if os.path.exists(os.getenv('APP_DIR') + "/lgsm/lock/backup.lock"):
            os.remove(os.getenv('APP_DIR') + "/lgsm/lock/backup.lock")
        discord_message("Backup in progress")
        os.chdir(os.getenv('APP_DIR'))
        subprocess.call(["./" + os.getenv('APP_EXECUTABLE'), "backup"])
        discord_message("Backup Successful")

    except:
        discord_message("An error occured while backuping the server. Please contact your administrator")
        sys.exit(1)


def start_server():
    try:
        subprocess.call([os.getenv('APP_DIR') + "/" + os.getenv('APP_EXECUTABLE'), "start"])
        discord_message("Server is started and running")

    except:
        discord_message("An error occured while starting the server. Please contact your administrator")
        sys.exit(1)


def main():
    discord_message("The server will restart in 5mn for daily maintenance. Please make sure to save yourr progress.")
    time.sleep(240)
    discord_message("The server will restart in 1mn for daily maintenance. Please make sure to save yourr progress.")
    time.sleep(60)

    stop_server()
    backup_server()
    start_server()


if __name__ == "__main__":
    main()
