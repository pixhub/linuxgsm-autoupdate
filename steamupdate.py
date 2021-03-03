import os
import subprocess
from subprocess import check_output
import re
import requests
import time
import sys
import datetime


def server_build_id():
    app_dir = os.getenv('APP_DIR')
    app_id = os.getenv('APP_ID')
    manifest = os.path.join(app_dir, "serverfiles/steamapps/appmanifest_" + app_id + ".acf")

    try:
        with open(manifest) as f:
            for line in f.readlines():
                if "buildid" in line:
                    server_build_id = re.sub("\D", "", line)
                    return server_build_id
                    break

    except:
        discord_message("Cannot retrieve server_build_id. Please contact you administrator")
        sys.exit(1)


def steam_build_id():
    steam_app_info = check_output(["steamcmd", 
                                "+login",
                                "anonymous",
                                "+app_info_print",
                                os.getenv("APP_ID"),
                                "+quit"])
    output = steam_app_info.decode()

    try:
        for line in output.split('\n'):
            if "buildid" in line:
                steam_build_id = re.sub("\D", "", line)
                return steam_build_id
                break

    except:
        discord_message("Cannot retrieve steam_build_id. Please contact you administrator")
        sys.exit(1)


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
        discord_message("An error occured while stopping the server. Please contact you administrator")
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
        discord_message("An error occured while backuping the server. Please contact you administrator")
        sys.exit(1)


def update_server():
    try:
        discord_message("Server update in progress")
        subprocess.call([os.getenv('APP_DIR') + "/" + os.getenv('APP_EXECUTABLE'), "update"])
        discord_message("Server successfuly updated")

    except:
        discord_message("An error occured while updating the server. Please contact you administrator")
        sys.exit(1)


def start_server():
    try:
        subprocess.call([os.getenv('APP_DIR') + "/" + os.getenv('APP_EXECUTABLE'), "start"])
        discord_message("Server is started and running")

    except:
        discord_message("An error occured while starting the server. Please contact you administrator")
        sys.exit(1)


def update_task():
    try:
        discord_message("The server will be shut down in 5mn for update purpose. Please make sure to save your progress.")
        time.sleep(240)
        discord_message("The server will be shut down in 1mn for update purpose. Please make sure to save your progress.")
        time.sleep(60)

        stop_server()
        backup_server()
        update_server()
        start_server()

    except:
        discord_message("An error occured during the updating process. Please contact you administrator")
        sys.exit(1)


def check_versions():
    if server_build_id() != steam_build_id():
        update_task()


def main():
    check_versions()


if __name__ == "__main__":
    main()
