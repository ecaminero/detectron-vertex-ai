from google.cloud import storage
from . import utils


def is_list(bucket: str):
    """ checking if it's a blob or a file """
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blobs = bucket.list_blobs()

    return isinstance(blobs, list)

def is_blob(bucket: str, file:str):
    """ checking if it's a blob """
    client = storage.Client()
    blob = client.get_bucket(bucket).get_blob(file)
    return hasattr(blob, 'exists') and callable(getattr(blob, 'exists'))


def get_blob(bucket: str, file:str):
    # Instantiates a client
    utils.create_tmp_folder()
    client = storage.Client()
    blob = client.get_bucket(bucket).get_blob(file)
    if blob.exists():
        destination_uri = '{}/{}'.format((utils.TMP_FOLDER), utils.get_img_name(blob.name)) 
        blob.download_to_filename(destination_uri)
        return destination_uri
    
    return None

def upload_to_bucket(bucket:str, name:str, file:str):
    # Instantiates a client
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(name)
    blob.upload_from_filename(filename=file)
    
    return blob.public_url
