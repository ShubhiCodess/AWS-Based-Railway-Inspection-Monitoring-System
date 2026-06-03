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

from fastapi import FastAPI
from ultralytics import YOLO

import boto3
from decimal import Decimal


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


# -------------------------
# CONFIG
# -------------------------

VALID_CLASSES = {
    0: "clipping",
    4: "seams",
    5: "sharp_rails"
}

CONF_THRESHOLD = 0.4

CLIPPING_ALERT_THRESHOLD = 15


# -------------------------
# ROUTES
# -------------------------

@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.post("/predict")
async def predict(data: dict):

    local_path = None
    output_path = None

    try:

        bucket = data["bucket"]
        key = data["key"]

        latitude = data.get(
            "latitude"
        )

        longitude = data.get(
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

        # -------------------
        # DOWNLOAD IMAGE
        # -------------------

        s3.download_file(
            bucket,
            key,
            local_path
        )

        # -------------------
        # RUN MODEL
        # -------------------

        results = model(
            local_path
        )

        summary = defaultdict(
            lambda: {
                "count": 0,
                "max_conf": 0
            }
        )

        # -------------------
        # FILTER + DRAW
        # -------------------

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

                    keep.append(i)

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

        # -------------------
        # CREATE OUTPUT
        # -------------------

        detections = []

        for cls, data in (
            summary.items()
        ):

            detections.append({

                "class":
                VALID_CLASSES[
                    cls
                ],

                "count":
                data[
                    "count"
                ],

                "max_confidence":
                Decimal(
                    str(
                        round(
                            data[
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
            clipping_count >
            CLIPPING_ALERT_THRESHOLD
        )

        # -------------------
        # UPLOAD RESULT
        # -------------------

        s3.upload_file(

            output_path,

            bucket,

            processed_key
        )

        # -------------------
        # SAVE DYNAMODB
        # -------------------

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
            (
                Decimal(
                    str(
                        latitude
                    )
                )
                if latitude
                else None
            ),

            "longitude":
            (
                Decimal(
                    str(
                        longitude
                    )
                )
                if longitude
                else None
            ),

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
