# 🎯 Multi-Purpose Object Tracking System

This project detects and tracks multiple objects in video footage using **YOLOv5** for detection and **SORT (Simple Online and Realtime Tracking)** for multi-object tracking. Each detected object is assigned a **unique ID** that remains consistent across frames. While demonstrated with football player tracking, this system is designed as a multipurpose tracking solution suitable for various applications including traffic monitoring, crowd analysis, and wildlife observation.

Football was specifically chosen as the demonstration case because it involves tracking many players (typically 22 on the field) with dynamic momentum and frequent interactions, making it an ideal showcase for the system's advanced tracking capabilities.

**Developed by:** Manoj Pentapati

---

## 🚀 Features

- Multi-object detection using **YOLOv5**
- Real-time tracking with **SORT algorithm**
- Unique ID assignment for each tracked object
- Interactive object selection by ID (supports multi-digit IDs like 21, 56, etc.)
- Enhanced popup window for focused object view
- On-screen statistics showing active object IDs
- Enhanced video quality with better resolution and reduced artifacts
- Scalable for tracking dozens to hundreds of objects
- Multipurpose design suitable for various tracking scenarios
- Works on **CPU (No GPU required)**

---

## 📁 Project Structure

```
object_Tracking_System/
│
├── object_tracker_gui.py    # Main interactive application with enhanced GUI
├── object_tracker_basic.py  # Basic tracker (non-interactive)
├── sort.py                 # SORT tracking algorithm
├── yolov5s.pt              # YOLOv5 pretrained weights
├── Football.mp4            # Sample input video
├── requirements.txt        # pip dependencies
├── environment.yml         # (Optional) conda environment file
├── README.md               # Project documentation
└── venv/                   # Python virtual environment (local)
```

---

## 🧠 How It Works

1. **YOLOv5** detects objects in each video frame
2. Bounding boxes are passed to **SORT**
3. SORT assigns and maintains **unique object IDs**
4. OpenCV renders bounding boxes, IDs and interactions
5. Optional object selection highlights a specific ID

The system is designed to handle complex scenarios with multiple moving objects, occlusions, and varying lighting conditions.

## 🔄 Recent Improvements

- **Enhanced Video Quality**: Improved resolution and reduced artifacts in displayed video
- **Multi-Digit ID Selection**: Can now select objects with IDs beyond single digits (e.g., 21, 56, 123)
- **Scalable Architecture**: Supports tracking dozens to hundreds of objects
- **Extended Use Cases**: Ready for both person tracking (football) and vehicle monitoring
- **Better User Experience**: Visual feedback during ID input and improved controls

## 🔍 Popup Window Feature

The enhanced popup window provides a detailed view of selected objects with superior image quality:

- **High-Resolution Display**: 400x400 pixel viewing area with sharp, clear imagery
- **Advanced Image Processing**: Unsharp masking and controlled sharpening for enhanced detail
- **Real-Time Updates**: Instant display of the selected object with minimal latency
- **Performance Optimized**: Lightweight processing maintains system responsiveness
- **Visual Benefits**: Clear identification of object characteristics, movements, and interactions

The popup window dynamically switches between a focused view of the selected object and an overview of the entire scene when no object is selected.

---

## ✅ System Requirements

- **Windows 10 / 11**
- **Python 3.12.x (Recommended: 3.12.10)**
- Minimum **8 GB RAM**
- No GPU required (CPU works fine)

> ⚠️ **Important**: Python 3.13 / 3.14 are **not recommended** due to library compatibility issues.

---

## 🔧 Installation Guide

### Method 1: Using pip with Virtual Environment (Recommended)

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate Environment**
   ```bash
   venv\Scripts\activate
   ```
   You should see `(venv)` in your command prompt.

3. **Install Dependencies**
   ```bash
   python -m pip install torch torchvision opencv-python matplotlib numpy Pillow PyYAML tqdm requests scipy pandas seaborn filterpy scikit-image lap ultralytics
   ```
   
   ✔ All packages install as prebuilt wheels
   ✔ No GCC / MSVC required
   ✔ No compilation errors

### Method 2: Using Conda (Alternative)

1. **Install Miniconda** (if not already installed)
   - Download from: https://docs.conda.io/en/latest/miniconda.html
   - Install with default settings

2. **Create Conda Environment**
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate Environment**
   ```bash
   conda activate object_tracker_env
   ```

---

## ▶️ Running the Application

### Interactive Soccer Tracker (Recommended)

```bash
python object_tracker_gui.py
``

**Controls:**
- Type multi-digit ID numbers (e.g., '3' then '1' for ID 31)
- `Enter`: Confirm ID selection
- `Backspace`/`Escape`: Clear input buffer
- `c`: Clear player selection
- `q`: Quit application

**Note:** After typing the digits, press `Enter` to confirm your selection. The system will now wait for your confirmation rather than selecting partial IDs.

### Basic Tracker (No Interaction)

```bash
python object_tracker_basic.py
```

**Controls:**
- `Esc`: Stop playback

---

## 🎥 Using Your Own Video

1. Copy your video file into the project folder

2. Either:
   - Rename your video to `Football.mp4` to use it directly, or
   - Update the `video_path` variable in the Python scripts:
     ```python
     video_path = "your_video.mp4"
     ```

---

## 🧪 Environment Verification (Optional)

To verify that all required packages are installed correctly:

```bash
python -c "import torch, cv2, numpy; print('Environment OK')"
```

---

## ⚠️ Common Issues & Fixes

### Issue: ModuleNotFoundError: ultralytics
**Solution:**
```bash
pip install ultralytics
```

### Issue: Video not opening
**Solutions:**
1. Ensure the video file exists in the project directory
2. Check that you're using the correct filename
3. Make sure you're running the command from the project directory

### Issue: CUDA / GPU errors
**Solution:**
- Ignore these errors
- The project automatically runs on CPU

### Issue: pip not found
**Solution:**
Always use:
```bash
python -m pip install ...
```

---

## ❌ What NOT to Do

- ❌ Do not use Python 3.14
- ❌ Do not install MSYS2 / GCC
- ❌ Do not mix Conda and pip in the same environment
- ❌ Do not rename model files arbitrarily

See `IMPROVEMENTS_SUMMARY.md` for details on recent enhancements to the application.

See `POPUP_WINDOW_ENHANCEMENT.md` for specific improvements to the player selection popup window.

---

## 📞 Support

## 🌍 Real-World Applications

This multipurpose object tracking system has numerous practical applications across various industries:

### Sports Analytics
- **Football/Soccer**: Player movement analysis, formation tracking, possession statistics
- **Basketball**: Player positioning, shot analysis, defensive coverage
- **Tennis**: Ball trajectory tracking, player movement patterns

### Traffic and Transportation
- **Vehicle Monitoring**: Traffic flow analysis, congestion detection, violation tracking
- **Pedestrian Safety**: Crowd monitoring, pedestrian flow analysis at crossings
- **Public Transit**: Passenger counting, queue management

### Security and Surveillance
- **Crowd Control**: Monitoring large gatherings, detecting unusual behavior
- **Perimeter Security**: Intrusion detection, boundary monitoring
- **Retail Analytics**: Customer movement tracking, heatmap generation for store layout optimization

### Wildlife and Environmental
- **Animal Behavior Studies**: Tracking animal movements in natural habitats
- **Conservation Efforts**: Monitoring endangered species populations
- **Agriculture**: Livestock monitoring, crop surveillance

### Industrial Applications
- **Manufacturing**: Assembly line product tracking, quality control
- **Logistics**: Inventory management, package tracking
- **Construction**: Equipment monitoring, worker safety compliance

## 🚀 Future Development Plans

We are continuously working to enhance the system with new features and capabilities:

### Short-Term Goals (Next 3-6 months)
- **Team Color Detection**: Automatic identification of team affiliations through uniform colors
- **Movement Analytics**: Velocity, acceleration, and distance metrics for tracked objects
- **Heatmap Generation**: Visualization of object positioning patterns over time
- **Configuration System**: External configuration files for easy parameter tuning

### Medium-Term Goals (6-12 months)
- **Graphical User Interface**: Professional desktop application with intuitive controls
- **Database Integration**: Storage and retrieval of tracking data for analysis
- **Export Capabilities**: Multiple formats (CSV, JSON, XML) for data sharing
- **Multi-Camera Support**: Coordination between multiple video sources

### Long-Term Vision (12+ months)
- **Deep Learning Enhancement**: Custom-trained models for specific use cases
- **Cloud Integration**: Remote processing and distributed computing
- **Mobile Platform**: iOS/Android applications for field use
- **API Development**: RESTful services for integration with other systems
- **Advanced Analytics**: Predictive modeling and behavioral analysis

These enhancements will transform the system into a comprehensive object tracking and analysis platform suitable for enterprise-level deployments.

If you encounter any issues not covered in this documentation, please ensure you've followed all installation steps correctly and have the proper system requirements.

**Developed by:** Manoj Pentapati
