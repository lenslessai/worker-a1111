import os
import glob
import boto3

def dir_size_in_mb(path):
    for path, dirs, files in os.walk(path):
        size = 0
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    
    print("models total size is " + str(size/1024/1024) + " mb")
    return size/1024/1024



def remove_3_oldest_files(path = "/runpod-volume/models/Lora"):
    print("Started to remove 3 oldest model files")
    files = glob.glob(os.path.join(path, '*'))
    files.sort(key=os.path.getmtime, reverse=True)

    for file_to_delete in files[:3]:
        try:
            os.remove(file_to_delete)
            print(f"Deleted: {file_to_delete}")
        except Exception as e:
            print(f"Error deleting {file_to_delete}: {str(e)}")

    print("Deletion complete.")



def download_model(user_id, model_name, model_name_in_volume):
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
    aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
    bucket_name = os.environ.get('BUCKET_PHOTOS')
    region = 'us-east-1'

    if aws_access_key_id is None or aws_secret_access_key is None:
        raise ValueError("AWS credentials not found in environment variables.")

    if bucket_name is None:
        raise ValueError("S3 bucket name not found in environment variables.")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

    s3 = session.client('s3')
    s3.download_file(bucket_name, "models/"+user_id+"/"+model_name, "/runpod-volume/models/Lora/"+model_name_in_volume)
    print(model_name_in_volume + " downloaded")


def remove_suffix_safetensors_suffix(input_string):
    if input_string.endswith(".safetensors"):
        return input_string[:-12]  # Remove the last 12 characters
    else:
        return input_string