"""
USAGE:
python test.py --img A_test.jpg
"""

import torch
import joblib
import torch.nn as nn
import numpy as np
import cv2
import argparse
import albumentations
import torch.nn.functional as F
import time
import cnn_models
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--img", default="A_test.jpg", type=str, help="path for the image to test on"
)
args = vars(parser.parse_args())

lb = joblib.load("../outputs/lb.pkl")

aug = albumentations.Compose(
    [
        albumentations.Resize(224, 224, always_apply=True),
    ]
)

model = cnn_models.CustomCNN()
model.load_state_dict(torch.load("../outputs/model.pth"))
print(model)
print("Model loaded")

image = cv2.imread(f"../input/asl_alphabet_test/asl_alphabet_test/{args['img']}")
image_copy = image.copy()

image = aug(image=np.array(image))["image"]
image = np.transpose(image, (2, 0, 1)).astype(np.float32)
image = torch.tensor(image, dtype=torch.float)
image = image.unsqueeze(0)
print(image.shape)

start = time.time()
outputs = model(image)
_, preds = torch.max(outputs.data, 1)
print("PREDS", preds)
print(f"Predicted output: {lb.classes_[preds]}")
end = time.time()
print(f"{(end-start):.3f} seconds")

cv2.putText(
    image_copy,
    lb.classes_[preds],
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (0, 0, 255),
    2,
)
plt.imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))
plt.show()
cv2.imwrite(f"../outputs/{args['img']}", image_copy)
cv2.waitKey(0)
