# utils/gcs_downloader.py
import os
from google.cloud import storage

def download_folder(bucket_name: str, prefix: str, local_dir: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        relative_path = blob.name[len(prefix):].lstrip('/')
        local_path = os.path.join(local_dir, relative_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"⬇️ Downloading {blob.name} → {local_path}")
        blob.download_to_filename(local_path)
