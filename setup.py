import os
import sys
import shutil

BROWSERSTACK_AUT_LOG_URL = "https://automate.browserstack.com/logs/"
BROWSERSTACK_AUT_SESSION_LOG_URL = "https://api.browserstack.com/automate/sessions/"
BROWSERSTACK_APP_AUT_SESSION_LOG_URL = "https://api-cloud.browserstack.com/app-automate/sessions/"

# essentially using environment variables to authenticate the agents.
try:
    AUTH = (os.environ["BROWSERSTACK_USERNAME"], os.environ["BROWSERSTACK_KEY"])
except KeyError:
    print("Ensure BROWSERSTACK_USERNAME and BROWSERSTACK_KEY has been set in environment variable.\n")
    print("Command to set environment variable.\n")
    print("export BROWSERSTACK_USERNAME='your_browserstack_username'.\n")
    print("export BROWSERSTACK_KEY='your_browserstack_key'.\n")
    print("source ~/.bash_profile")
    sys.exit(1) # kills the app with the above info

try:
    os.mkdir('uploads')
    os.mkdir('downloads')
except FileExistsError:
    pass


try:
    # as per my understanding, the below code is used to create two folders on our local machine to store data.
    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'  # run os.path.dirname() for clarity
    DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
except Exception:
    pass

# below function is used multiple times in main_app.py
def remove_and_create_download_folder():
    # shutil is a high level file operation module in Python. rmtree deletes the entire DOWNLOAD_FOLDER
    shutil.rmtree(DOWNLOAD_FOLDER)
    os.mkdir('downloads') # creating the downloads folder again
