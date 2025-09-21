import io
import cv2
import numpy as np
from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image

# Initialize the Flask application
app = Flask(__name__)

# Load the YOLOv8 model once when the server starts
try:
    model = YOLO("best.pt")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    # Exit if the model can't be loaded
    exit()

def sort_detections_column_major(detections, class_names):
    """
    Sorts detections top-to-bottom, then left-to-right.
    Returns a list of dictionaries with structured data.
    """
    if not detections:
        return []

    # Calculate average width for thresholding columns
    avg_width = np.mean([det[2] - det[0] for det in detections])
    x_threshold = avg_width * 0.7

    # Sort detections primarily by their x-coordinate
    detections.sort(key=lambda d: d[0])

    # Group detections into columns based on x-coordinate
    columns = []
    if detections:
        current_column = [detections[0]]
        for i in range(1, len(detections)):
            prev_det_x_center = (detections[i-1][0] + detections[i-1][2]) / 2
            current_det_x_center = (detections[i][0] + detections[i][2]) / 2
            
            if (current_det_x_center - prev_det_x_center) > x_threshold:
                columns.append(current_column)
                current_column = [detections[i]]
            else:
                current_column.append(detections[i])
        columns.append(current_column)

    # Sort each column by the y-coordinate (top-to-bottom)
    for col in columns:
        col.sort(key=lambda d: d[1])

    sorted_results = []
    question_number = 1
    for col in columns:
        for det in col:
            x1, y1, x2, y2, conf, cls_id = det
            full_class_name = class_names[int(cls_id)]
            
            # --- THIS IS THE CHANGED PART ---
            # Split the class name by space and take the last part
            # This turns "CLASS A" into "A"
            answer_letter = full_class_name.split(' ')[-1]
            
            sorted_results.append({
                "question": question_number,
                "answer": answer_letter  # Use the extracted letter
            })
            question_number += 1
            
    return sorted_results

@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint to receive an image and return YOLOv8 predictions.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No image selected for uploading'}), 400

    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img_np = np.array(img)
        results = model(img_np)
        
        detections = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls_id = box.cls[0].item()
            conf = box.conf[0].item()
            detections.append((x1, y1, x2, y2, conf, cls_id))
        
        class_names = results[0].names
        sorted_predictions = sort_detections_column_major(detections, class_names)
        
        return jsonify({'predictions': sorted_predictions})

    except Exception as e:
        return jsonify({'error': f'Error during prediction: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)