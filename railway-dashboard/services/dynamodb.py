import boto3
import os
from dotenv import load_dotenv

load_dotenv()

table_name=os.getenv(
    "DYNAMODB_TABLE"
)

region=os.getenv(
    "AWS_REGION"
)

db=boto3.resource(
    "dynamodb",
    region_name=region
)

table=db.Table(
    table_name
)


def get_records():

    items=[]

    response=table.scan()

    items.extend(
        response["Items"]
    )

    while "LastEvaluatedKey" in response:

        response=table.scan(

            ExclusiveStartKey=

            response[
                "LastEvaluatedKey"
            ]
        )

        items.extend(
            response[
                "Items"
            ]
        )

    return items
