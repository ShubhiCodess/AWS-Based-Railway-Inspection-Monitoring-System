import boto3

BUCKET_NAME = "railway-crack-images-esp"
FILE_NAME = "test1.jpg"

s3 = boto3.client('s3')

try:
    s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    print("✅ Upload successful")
except Exception as e:
    print("❌ Error:", e)