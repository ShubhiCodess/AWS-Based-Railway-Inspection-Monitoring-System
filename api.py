```python
import sys
import os

sys.path.insert(
    0,
    os.path.abspath("ultralytics_mod")
)

import cv2
import uuid
from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from fastapi import FastAPI
from ultralytics import YOLO

import boto3


app = FastAPI()

model = YOLO("best.pt")

s3 = boto3.client("s3")

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-south-1"
)

table = dynamodb.Table(
    "railway_detections"
)


VALID_CLASSES = {

    0: "clipping",

    4: "seams",

    5: "sharp_rails"
}

CONF_THRESHOLD = 0.4

CLIPPING_ALERT_THRESHOLD = 15


@app.get("/")
def home():

    return {

        "status":
        "running"
    }


@app.post("/predict")
async def predict(payload: dict):

    local_path = None

    output_path = None

    try:

        bucket = payload["bucket"]

        key = payload["key"]

        latitude = payload.get(
            "latitude"
        )

        longitude = payload.get(
            "longitude"
        )

        detection_id = str(
            uuid.uuid4()
        )

        local_path = (
            f"/tmp/{detection_id}.jpg"
        )

        output_path = (
            f"/tmp/out_{detection_id}.jpg"
        )

        processed_key = (
            f"processed/{detection_id}.jpg"
        )

        s3.download_file(

            bucket,

            key,

            local_path
        )

        results = model(
            local_path
        )

        summary = defaultdict(

            lambda: {

                "count": 0,

                "max_conf": 0
            }
        )

        for r in results:

            keep = []

            for i, box in enumerate(
                r.boxes
            ):

                cls = int(
                    box.cls[0]
                )

                conf = float(
                    box.conf[0]
                )

                if (

                    cls in VALID_CLASSES

                    and

                    conf >= CONF_THRESHOLD
                ):

                    keep.append(
                        i
                    )

                    summary[
                        cls
                    ][
                        "count"
                    ] += 1

                    summary[
                        cls
                    ][
                        "max_conf"
                    ] = max(

                        summary[
                            cls
                        ][
                            "max_conf"
                        ],

                        conf
                    )

            filtered = r[keep]

            annotated = (
                filtered.plot()
            )

            cv2.imwrite(

                output_path,

                annotated
            )

        detections = []

        for cls, stats in (
            summary.items()
        ):

            detections.append({

                "class":
                VALID_CLASSES[
                    cls
                ],

                "count":
                stats[
                    "count"
                ],

                "max_confidence":

                Decimal(

                    str(

                        round(

                            stats[
                                "max_conf"
                            ],

                            3
                        )
                    )
                )
            })

        clipping_count = (
            summary[0]["count"]
        )

        alert = (

            clipping_count

            >

            CLIPPING_ALERT_THRESHOLD
        )

        s3.upload_file(

            output_path,

            bucket,

            processed_key
        )

        item = {

            "detection_id":
            detection_id,

            "timestamp":
            datetime.utcnow()
            .isoformat(),

            "original_image":
            key,

            "processed_image":
            processed_key,

            "latitude":

            Decimal(
                str(
                    latitude
                )
            )

            if latitude

            else None,

            "longitude":

            Decimal(
                str(
                    longitude
                )
            )

            if longitude

            else None,

            "detections":
            detections,

            "alert":
            alert
        }

        table.put_item(
            Item=item
        )

        return {

            "status":
            "success",

            "record":
            item
        }

    except Exception as e:

        return {

            "status":
            "error",

            "message":
            str(e)
        }

    finally:

        if (

            local_path

            and

            os.path.exists(
                local_path
            )
        ):

            os.remove(
                local_path
            )

        if (

            output_path

            and

            os.path.exists(
                output_path
            )
        ):

            os.remove(
                output_path
            )


@app.post("/predict-folder")
async def predict_folder(payload: dict):

    try:

        bucket = payload["bucket"]

        prefix = payload["prefix"]

        latitude = payload.get(
            "latitude"
        )

        longitude = payload.get(
            "longitude"
        )

        response = s3.list_objects_v2(

            Bucket=bucket,

            Prefix=prefix
        )

        processed = []

        for obj in response.get(
            "Contents",
            []
        ):

            key = obj["Key"]

            if key.endswith("/"):

                continue

            result = await predict({

                "bucket":
                bucket,

                "key":
                key,

                "latitude":
                latitude,

                "longitude":
                longitude
            })

            processed.append({

                "image":
                key,

                "status":
                result.get(
                    "status"
                ),

                "message":
                result.get(
                    "message"
                )
            })

        return {

            "status":
            "success",

            "processed":
            len(
                processed
            ),

            "images":
            processed
        }

    except Exception as e:

        return {

            "status":
            "error",

            "message":
            str(e)
        }
```

