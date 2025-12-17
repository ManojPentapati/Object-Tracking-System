import cv2
import torch
from sort import Sort
import numpy as np
import sys

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Set OpenCV window properties for better quality
# For vehicle tracking or other applications, we can detect different classes
class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat']

# Load the video file (make sure it's in the same directory or give full path)
# Using relative path for video file - make sure Football.mp4 is in the same directory
video_path = 'Football.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not find video file.")
    exit()

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Resolution: {width}x{height}, FPS: {fps}")
print("Starting video processing...")

# Define video writer to save output
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Initialize SORT tracker
tracker = Sort()

# Create window with better quality settings
cv2.namedWindow('YOLOv5 + SORT Tracking', cv2.WINDOW_NORMAL)
cv2.resizeWindow('YOLOv5 + SORT Tracking', 1200, 700)
# Set window properties for better rendering
cv2.setWindowProperty('YOLOv5 + SORT Tracking', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference with autoshape (resizing and normalization handled internally)
    with torch.no_grad():
        results = model(frame)

    # Get detections - can be configured for different object types
    detections = results.xyxy[0].cpu().numpy()
    # For football tracking: person class (0)
    # For vehicle tracking: car class (2), bus class (5), truck class (7)
    # Here we'll keep person detection for consistency with the main app
    person_detections = detections[detections[:, 5] == 0]
    detections_for_sort = person_detections[:, :5]  # x1, y1, x2, y2, confidence

    # Track objects using SORT
    tracked_objects = tracker.update(detections_for_sort)

    # Draw boxes and labels with better formatting
    for *box, obj_id in tracked_objects:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'ID: {int(obj_id)}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Display statistics
    current_ids = [int(obj[4]) for obj in tracked_objects]
    stats_text = f'Total Objects: {len(current_ids)}'
    cv2.putText(frame, stats_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show the frame with enhanced quality
    # Apply slight sharpening for better clarity
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    frame_sharpened = cv2.filter2D(frame, -1, kernel)
    frame_resized = cv2.resize(frame_sharpened, (min(width, 1200), min(height, 700)), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('YOLOv5 + SORT Tracking', frame_resized)
    out.write(frame)
    
    if cv2.waitKey(1) == 27:  # Press Esc to stop
        break

cap.release()
out.release()
cv2.destroyAllWindows()