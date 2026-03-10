import requests
import zipfile
import io
import os

url = "https://github.com/rongardF/tvdatafeed/archive/refs/heads/main.zip"
print(f"Downloading {url}...")
r = requests.get(url)
if r.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
        zip_ref.extractall("tvdatafeed_lib")
    print("Extracted to tvdatafeed_lib")
else:
    print(f"Failed to download: {r.status_code}")
