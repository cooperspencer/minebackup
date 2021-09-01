from googleapiclient.http import MediaFileUpload
from Google import Create_Service
from datetime import datetime
import os
import shutil
import bios

filepath = os.path.dirname(os.path.realpath(__file__))

conf = bios.read(f"{filepath}/conf.yml")

now = datetime.now()
nowstring = now.strftime("%Y-%m-%d_%H:%M:%S")
backupname = "{}/server_{}".format(conf["backuppath"], nowstring)

print("create {}.zip".format(backupname))

shutil.make_archive(backupname, 'zip', conf["minecraft"])

print("created {}.zip".format(backupname))

print("uploading {}.zip to google drive".format(backupname))

if not os.path.exists(conf["secretfile"]):
    conf["secretfile"] = f"{filepath}/{conf['secretfile']}"

CLIENT_SECRET_FILE = conf["secretfile"]
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

base = os.path.basename("{}.zip".format(backupname))

# Upload a file
file_metadata = {
    'name': base,
    'parents': [conf["parentdirectory"]]
}

media_content = MediaFileUpload("{}.zip".format(backupname), mimetype='application/zip', resumable=True, chunksize=1024 * 1024)

file = service.files().create(
    body=file_metadata,
    media_body=media_content
).execute()

print(file)