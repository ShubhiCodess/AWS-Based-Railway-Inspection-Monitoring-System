import pandas as pd


def flatten(records):

    rows=[]

    for r in records:

        total=0

        classes=[]

        for d in r["detections"]:

            total+=int(
                d["count"]
            )

            classes.append(
                d["class"]
            )

        rows.append({

            "timestamp":
            r["timestamp"],

            "detection_id":
            r["detection_id"],

            "original":
            r["original_image"],

            "processed":
            r["processed_image"],

            "alert":
            r["alert"],

            "classes":
            ",".join(
                classes
            ),

            "detections":
            total
        })

    return pd.DataFrame(
        rows
    )
