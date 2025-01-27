"""
USAGE:
python cam_test.py 
"""

import torch
import joblib
import torch.nn as nn
import numpy as np
import cv2
import argparse
import torch.nn.functional as F
import time
import cnn_models
import matplotlib.pyplot as plt


from torchvision import models

lb = joblib.load("../outputs/lb.pkl")

model = cnn_models.CustomCNN()
model.load_state_dict(torch.load("../outputs/model.pth"))
print(model)
print("Model loaded")


def hand_area(img):
    hand = img[100:324, 100:324]
    hand = cv2.resize(hand, (224, 224))
    return hand


cap = cv2.VideoCapture(0)

if cap.isOpened() == False:
    print("Error while trying to open camera. Plese check again...")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter(
    "../outputs/asl.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    30,
    (frame_width, frame_height),
)

while cap.isOpened():
    ret, frame = cap.read()
    cv2.rectangle(frame, (100, 100), (324, 324), (20, 34, 255), 2)
    hand = hand_area(frame)

    image = hand

    image = np.transpose(image, (2, 0, 1)).astype(np.float32)
    image = torch.tensor(image, dtype=torch.float)
    image = image.unsqueeze(0)

    outputs = model(image)
    _, preds = torch.max(outputs.data, 1)

    cv2.putText(
        frame,
        lb.classes_[preds],
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        2,
    )
    cv2.imshow("image", frame)
    out.write(frame)

    if cv2.waitKey(27) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()
