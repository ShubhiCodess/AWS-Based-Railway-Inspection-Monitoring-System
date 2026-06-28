
# Cloud-Native Railway Track Defect Detection System

An end-to-end cloud-based railway track inspection system that automatically detects defects using a custom-trained YOLO model deployed on AWS. The project combines robotics, computer vision, AWS cloud computing, and real-time monitoring into a scalable inspection pipeline.

---

##  Overview

Manual railway track inspection is slow, expensive, and prone to human error. This project automates the inspection process by continuously capturing railway track images from a mobile rover, uploading them to AWS S3, processing them using a YOLO model hosted on Amazon EC2, and visualizing detections through a live Streamlit dashboard.

The entire workflow is event-driven and designed for near real-time monitoring.

---

##  System Architecture

          Rover (Laptop/ESP32-CAM)
                    │
             Upload Images
                    │
                    ▼
              Amazon S3 Bucket
                    │
      (Dashboard Button Trigger)
                    │
                    ▼
          FastAPI Server (EC2)
                    │
        Watches for New Images
                    │
                    ▼
      YOLOv8 Defect Detection Model
                    │
        Bounding Boxes + Metadata
                    │
         Save Results to DynamoDB
                    │
                    ▼
         Streamlit Dashboard
      Live Detection Visualization


##  Features

* Automated railway track defect detection
* Cloud-native architecture using AWS
* FastAPI REST API hosted on EC2
* Continuous S3 image monitoring
* Real-time inference with YOLO
* Detection metadata stored in DynamoDB
* Live Streamlit dashboard
* Automatic annotation generation
* Scalable event-driven workflow
* Modular deployment

---

##  AI Model

The detection model is based on a customized YOLO architecture trained specifically for railway defects.
~ [Custom YOLO Model Repository](https://github.com/ShubhiCodess/Crack-Detection-in-Railway-Tracks)

### Model Enhancements

* SPD-Conv for preserving small defect information
* EMA Attention for enhanced feature extraction
* PAN-FPN feature fusion
* Custom dataset training
* Optimized for small object detection

### Dataset

* 7000+ annotated railway images
* Multiple railway defect classes
* Custom preprocessing and cleaning
* Data augmentation

---

##  AWS Services Used

| Service         | Purpose                          |
| --------------- | -------------------------------- |
| Amazon EC2      | Hosts FastAPI and YOLO inference |
| Amazon S3       | Image storage                    |
| Amazon DynamoDB | Detection metadata storage       |
| IAM             | Secure AWS access                |
| Boto3           | AWS SDK integration              |

---

##  Dashboard

The Streamlit dashboard provides:

* Live inspection status
* Detection statistics
* Annotated images
* Confidence scores
* Defect history
* Cloud status monitoring

---

##  Workflow

1. Rover captures railway images.
2. Images are uploaded to Amazon S3.
3. Dashboard sends a request to start inference.
4. FastAPI on EC2 continuously watches the S3 bucket.
5. New images are downloaded automatically.
6. YOLO performs defect detection.
7. Annotated images are generated.
8. Detection metadata is stored in DynamoDB.
9. Dashboard fetches results in real time.

---

##  Technologies Used

### Programming

* Python

### AI

* YOLOv8
* OpenCV
* Ultralytics

### Cloud

* AWS EC2
* AWS S3
* AWS DynamoDB
* Boto3

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit

---

##  Future Improvements

* SNS notifications
* Multi-camera support
* Video stream processing
* GPS tagging
* Predictive maintenance analytics
* Docker deployment
* Kubernetes orchestration

---

