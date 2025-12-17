import cv2
import numpy as np
import torch
from sort import Sort
import sys

# Initialize YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()

# Initialize SORT tracker
tracker = Sort()

# Video setup
# Using relative path for video file - make sure Football.mp4 is in the same directory
video_path = 'Football1.mp4'
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file. Make sure 'Football.mp4' is in the same directory as this script.")
    print("Available video files in current directory:")
    import os
    video_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
    for vf in video_files:
        print(f"  - {vf}")
    exit()

video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Video width: {video_width}, Video height: {video_height}, FPS: {fps}")

# Tracking variables
selected_id = None
current_ids = set()
track_history = {}

# Multi-digit input buffer for ID selection
input_buffer = ""
buffer_timeout = 0

# Create OpenCV windows with better quality settings
cv2.namedWindow('Soccer Game', cv2.WINDOW_NORMAL)
cv2.namedWindow('Player View', cv2.WINDOW_NORMAL)
# Set initial window sizes for better visibility
cv2.resizeWindow('Soccer Game', 1200, 700)
cv2.resizeWindow('Player View', 400, 400)
# Set window properties for better rendering
# Enable high quality rendering
cv2.setWindowProperty('Soccer Game', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Player View', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL)

def update_popup(frame, tracked_objects):
    global selected_id
    
    if selected_id is None or selected_id not in current_ids:
        # Show entire frame if no player is selected with superior quality
        popup_frame = cv2.resize(frame, (400, 400), interpolation=cv2.INTER_CUBIC)
        
        # Apply light enhancement for better visibility without blurring
        # Gentle noise reduction
        popup_frame = cv2.bilateralFilter(popup_frame, 7, 40, 40)
        
        # Apply CLAHE for better contrast
        lab = cv2.cvtColor(popup_frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
        l = clahe.apply(l)
        merged = cv2.merge([l, a, b])
        popup_frame = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
        
        # Light sharpening for better clarity
        kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
        popup_frame = cv2.filter2D(popup_frame, -1, kernel)
    else:
        # Find and focus on selected player
        for obj in tracked_objects:
            obj_id = int(obj[4])
            if obj_id == selected_id:
                x1, y1, x2, y2 = map(int, obj[:4])
                # Add padding around the player
                pad_x = int((x2 - x1) * 0.5)
                pad_y = int((y2 - y1) * 0.5)
                x1, y1 = max(0, x1 - pad_x), max(0, y1 - pad_y)
                x2, y2 = min(video_width, x2 + pad_x), min(video_height, y2 + pad_y)
                
                # Extract and process player region
                popup_frame = frame[y1:y2, x1:x2]
                if popup_frame.size == 0:
                    popup_frame = frame  # Fallback if region is invalid
                
                # Enhance the player image with superior sharpness and clarity
                # Further reduced resolution for better performance while maintaining detail
                popup_frame = cv2.resize(popup_frame, (400, 400), interpolation=cv2.INTER_CUBIC)
                
                # Preserve original sharpness by reducing aggressive filtering
                # Light noise reduction to minimize blur
                popup_frame = cv2.bilateralFilter(popup_frame, 9, 50, 50)
                
                # Apply unsharp masking for enhanced sharpness
                # Create a blurred version
                blurred = cv2.GaussianBlur(popup_frame, (0, 0), 3)
                # Subtract blurred from original to get mask
                mask = cv2.subtract(popup_frame, blurred)
                # Add mask back to original for sharpening effect
                popup_frame = cv2.addWeighted(popup_frame, 1.3, mask, 0.3, 0)
                
                # Apply adaptive histogram equalization for better contrast without losing details
                lab = cv2.cvtColor(popup_frame, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                l = clahe.apply(l)
                merged = cv2.merge([l, a, b])
                popup_frame = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
                
                # Final sharpening with controlled intensity
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                popup_frame = cv2.filter2D(popup_frame, -1, kernel)
                
                # Slight contrast enhancement
                popup_frame = cv2.convertScaleAbs(popup_frame, alpha=1.1, beta=2)
                break
    
    cv2.imshow('Player View', popup_frame)

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or unable to read the frame.")
        break
    
    # Object detection
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()
    # Filter only persons (class 0 in YOLOv5)
    detections = detections[detections[:, 5] == 0]
    detections = np.hstack((detections[:, :4], detections[:, 4:5]))
    
    # Object tracking
    tracked_objects = tracker.update(detections)
    
    # Update current IDs
    current_ids.clear()
    for obj in tracked_objects:
        current_ids.add(int(obj[4]))
    
    # Draw bounding boxes and IDs
    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = obj
        obj_id = int(obj_id)
        
        # Highlight selected player
        if selected_id is not None and obj_id == selected_id:
            color = (0, 0, 255)  # Red for selected player
            thickness = 3
        else:
            color = (0, 255, 0)  # Green for other players
            thickness = 2
        
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
        cv2.putText(frame, f"ID: {obj_id}", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Display statistics with better formatting
    active_ids = sorted(list(current_ids))
    ids_display = ', '.join(map(str, active_ids[:15]))  # Show first 15 IDs
    if len(active_ids) > 15:
        ids_display += f" ... (+{len(active_ids) - 15} more)"
    stats_text = f"Active IDs: {ids_display} | Total Objects: {len(current_ids)}"
    cv2.putText(frame, stats_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Display input buffer if active
    if input_buffer:
        buffer_text = f"Enter ID: {input_buffer}_"
        cv2.putText(frame, buffer_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Update displays
    # Show the frame with enhanced quality
    # Apply slight sharpening for better clarity
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    frame_sharpened = cv2.filter2D(frame, -1, kernel)
    cv2.imshow('Soccer Game', frame_sharpened)
    update_popup(frame, tracked_objects)
    
    # Handle key presses with multi-digit input support
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):  # Quit
        break
    elif 48 <= key <= 57:  # ASCII for '0' to '9'
        # Add digit to input buffer
        input_buffer += str(key - 48)
        buffer_timeout = 30  # Reset timeout (approx 1 second at 30 FPS)
        print(f"Input buffer: {input_buffer}")
        
        # Don't try to parse as complete ID immediately
        # Wait for Enter key or timeout to evaluate
        pass  # Just add to buffer and wait for confirmation
            
    elif key == ord('c'):  # Clear selection and buffer
        selected_id = None
        input_buffer = ""
        buffer_timeout = 0
        print("Cleared selection and input buffer")
    elif key == 8 or key == 27:  # Backspace (ASCII 8) or Escape
        # Clear input buffer
        input_buffer = ""
        buffer_timeout = 0
        print("Cleared input buffer")
    elif key == 13:  # Enter key
        # Force evaluation of current buffer
        if input_buffer:
            try:
                entered_id = int(input_buffer)
                if entered_id in current_ids:
                    selected_id = entered_id
                    print(f"Tracking object ID: {selected_id}")
                else:
                    print(f"Object ID {entered_id} not found in current frame.")
            except ValueError:
                print("Invalid ID entered")
            input_buffer = ""  # Clear buffer after evaluation
    
    # Decrement buffer timeout
    if buffer_timeout > 0:
        buffer_timeout -= 1
    else:
        # Clear buffer after timeout without selecting
        if input_buffer:
            print(f"Input timeout - clearing buffer: {input_buffer}")
            input_buffer = ""

# Cleanup
cap.release()
cv2.destroyAllWindows()