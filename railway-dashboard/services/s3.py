import boto3
import io
import os

from dotenv import load_dotenv
from PIL import Image

load_dotenv()

bucket=os.getenv(
    "S3_BUCKET"
)

client=boto3.client(
    "s3"
)


def get_image(key):

    obj=client.get_object(

        Bucket=bucket,

        Key=key
    )

    return Image.open(

        io.BytesIO(

            obj[
                "Body"
            ].read()
        )
    )
