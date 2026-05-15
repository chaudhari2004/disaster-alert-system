import boto3

s3 = boto3.client(
    's3',
    region_name='ap-south-1'
)

BUCKET_NAME = 'vivek-disaster-images-2026'

def upload_file(file, filename):

    s3.upload_fileobj(
        file,
        BUCKET_NAME,
        filename
    )

    image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

    return image_url