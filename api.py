import sys
import os
import uuid
from fastapi import FastAPI
from ultralytics import YOLO
import boto3
import cv2

# Force custom YOLO
sys.path.insert(
    0,
    os.path.abspath("ultralytics_mod")
)

app = FastAPI()

print("Loading model...")

model = YOLO("best.pt")

print("Model loaded.")

s3 = boto3.client("s3")


@app.get("/")  #to check if server on
def home():
    return {
        "status": "running"
    }

@app.post("/predict")
async def predict(data: dict):

    try:
        bucket = data["bucket"]
        key = data["key"]
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        detection_id = str(uuid.uuid4())

        local_path = f"/tmp/{detection_id}.jpg"
        output_path = f"/tmp/out_{detection_id}.jpg"
        processed_key = f"processed/{detection_id}.jpg"

        s3.download_file(bucket,key,local_path)

        results = model(local_path)
        detections = []
        for r in results:
            annotated = r.plot()
            cv2.imwrite(output_path,annotated)
                
        for box in r.boxes:
            detections.append({
                "class_id":int(box.cls[0]),
                "confidence":Decimal(str(float(box.conf[0])))
                })

        s3.upload_file(output_path,bucket,processed_key)

        item = {
            "detection_id":detection_id,
            "timestamp":datetime.utcnow().isoformat(),
            "original_image":key,
            "processed_image":processed_key,
            "latitude":Decimal(str(latitude))
            if latitude else None,
            "longitude":Decimal(str(longitude))
            if longitude else None,
            "detections":detections
        }

        table.put_item(
            Item=item
        )

        if os.path.exists(local_path):os.remove(local_path)
        if os.path.exists(output_path):os.remove(output_path)
        return {

            "status":"success",
            "record":item
        }

    except Exception as e:
        return {
            "status":"error",
            "message":str(e)
        }
