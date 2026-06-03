import sys
import os

sys.path.insert(
    0,
    os.path.abspath("ultralytics_mod")
)

from ultralytics import YOLO

model = YOLO("best.pt")

results = model("test-rail.jpg")

print(results)
