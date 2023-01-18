import os
import boto3
import numpy as np
from PIL import Image
from io import BytesIO

# This function takes the name of the bucket as input and returns the filenames inside the bucket.
def list_s3_files_using_client(s3, bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = response.get("Contents")
        for file in files:
            print(f"bucket: {bucket_name}, file_name: {file['Key']}, size: {file['Size']}")
        return files
    except:
        print("Files could not be read.")
        return None

# This function takes the bucket and image name as input and returns the image as PIL format.
def read_image_from_s3(bucket, key):
    try:
        object = bucket.Object(key)
        response = object.get()
        file_stream = response['Body']
        im = Image.open(file_stream)
        return im
    except:
        print("The image could not be read. The file may not be an image.")
        return None

# This function takes bucket and image as input and uploads image to bucket
def write_image_to_s3(img, bucket, key):
    try:
        object = bucket.Object(key)
        file_stream = BytesIO()
        img.save(file_stream, format='jpeg')
        object.put(Body=file_stream.getvalue())
    except:
        print("Image could not be uploaded to cloud.")

# This function takes image as input and checks transparent pixels
def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False


# For AWS session connection
AWS_SERVER_PUBLIC_KEY = "AKIAWUOAJXUET3RLZEUT"
AWS_SERVER_SECRET_KEY = "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"

source_bucket_name = "data-engineer-takehome-test-source-storage"
destination_bucket_name = "data-engineer-takehome-test-destination-storage"

# AWS Conection
session = boto3.Session(
    aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key=AWS_SERVER_SECRET_KEY,
)


s3_client = session.client('s3')
s3_resource = session.resource('s3')
soruce_bucket = s3_resource.Bucket(source_bucket_name)
destination_bucket = s3_resource.Bucket(destination_bucket_name)

# File for transparent image names
transparent_file = open("transparent_ones.txt", "a") 

# File names in the bucket
files = list_s3_files_using_client(s3_client, source_bucket_name)

# File names in the bucket
for file in files:
    # Read single image from bucket
    image = read_image_from_s3(soruce_bucket, file['Key'])
    if image != None:
        # Check transparency
        isTransparent = has_transparency(image)
        print(file['Key'], ": ", isTransparent)
        if isTransparent:
            # Write image name to file
            transparent_file.write(file['Key'] + "\n")
        else:
            # Write image to s3 bucket
            write_image_to_s3(image, destination_bucket, file['Key'])
    
# Files in destination bucket
files = list_s3_files_using_client(s3_client, destination_bucket_name)
transparent_file.close()

