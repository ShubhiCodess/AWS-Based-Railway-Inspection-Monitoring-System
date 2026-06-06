import os
import time
import json
import hashlib
import boto3
from pathlib import Path

WATCH_FOLDER="track-images"
BUCKET = "railway-crack-images-esp"
S3_PREFIX = "raw/"
CHECK_INTERVAL = 3
WATCH_DURATION_MIN = 5
TRACK_FILE = "uploaded_db.json"

VALID = {".jpg", ".jpeg", ".png"}


s3 = boto3.client( "s3")

if os.path.exists(TRACK_FILE):
    with open(TRACK_FILE,"r") as f:
        uploaded = json.load(f)
else:
    uploaded = {}

def save_db():
    with open(TRACK_FILE,"w") as f:
        json.dump(uploaded,f,indent=2)

def file_hash(path):

    h = hashlib.md5()
    with open(path,"rb") as f:

        while True:
            chunk = f.read( 8192)

            if not chunk: break
            h.update(chunk)

    return h.hexdigest()



def stable(path):

    try:

        a = os.path.getsize(path)

        time.sleep(1)

        b = os.path.getsize( path)
        return a == b

    except:
        return False


def upload(path):

    abs_path = str(Path(path).resolve())

    current_hash = (file_hash(path))

    if (abs_path in uploaded and uploaded[abs_path] == current_hash):
        return

    rel = os.path.relpath(path,WATCH_FOLDER)

    key = (S3_PREFIX+rel.replace("\\","/"))

    try:
        print(f"Uploading {key}" )
        s3.upload_file(path,BUCKET,key)
        uploaded[abs_path] = current_hash
        save_db()
        print("Uploaded")

    except Exception as e:
        print(e)

def scan():

    for root, _, files in os.walk( WATCH_FOLDER):

        for file in files:
            path = os.path.join(root,file)
            ext = ( Path(path).suffix.lower())
            if ext not in VALID:
                continue
            if not stable(path):
                continue
            upload(path)


print("\nMonitoring started...")

end = (time.time()+WATCH_DURATION_MIN* 60)

while (time.time()<end):
    scan()
    time.sleep(CHECK_INTERVAL)

print(
    "\nMonitoring finished."
)
