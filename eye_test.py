import cv2
import mediapipe as mp
import numpy as np
import random
import time

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Define eye landmarks (left and right)
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
LEFT_IRIS_INDICES = [468, 469, 470, 471, 472]
RIGHT_IRIS_INDICES = [473, 474, 475, 476, 477]

# All 8 possible gaze directions
directions = ["Left", "Right", "Up", "Down", 
              "Up-Left", "Up-Right", "Down-Left", "Down-Right"]
direction_vectors = {
    "Left": (-1, 0),
    "Right": (1, 0),
    "Up": (0, -1),
    "Down": (0, 1),
    "Up-Left": (-1, -1),
    "Up-Right": (1, -1),
    "Down-Left": (-1, 1),
    "Down-Right": (1, 1)
}

def get_gaze_ratio(eye_landmarks, iris_landmarks, frame_shape):
    """Calculate gaze direction ratios for one eye"""
    eye_region = np.array([(landmark[0], landmark[1]) for landmark in eye_landmarks])
    x_min, y_min = np.min(eye_region, axis=0)
    x_max, y_max = np.max(eye_region, axis=0)
    
    iris_center = np.mean(iris_landmarks, axis=0)
    
    x_ratio = (iris_center[0] - x_min) / (x_max - x_min)
    y_ratio = (iris_center[1] - y_min) / (y_max - y_min)
    
    return x_ratio, y_ratio

def determine_gaze_direction(x_ratio, y_ratio):
    """Determine gaze direction based on normalized ratios"""
    horizontal = ""
    vertical = ""
    
    if x_ratio < 0.4:
        horizontal = "Left"
    elif x_ratio > 0.6:
        horizontal = "Right"
        
    if y_ratio < 0.4:
        vertical = "Up"
    elif y_ratio > 0.6:
        vertical = "Down"
    
    if not horizontal and not vertical:
        return "Center"
    
    direction = f"{vertical}-{horizontal}" if vertical and horizontal else f"{vertical}{horizontal}"
    return direction.replace("--", "-").strip("-")

def is_face_inside_frame(image, bbox, margin=50):
    img_h, img_w = image.shape[:2]
    x_min, y_min, x_max, y_max = bbox
    return (x_min > margin and y_min > margin and
            x_max < img_w - margin and y_max < img_h - margin)

# Main execution
cap = cv2.VideoCapture(0)
test_started = False
test_completed = False
instruction_delay = 3  # Increased delay for better user experience
current_instruction = ""
match_result = ""
last_instruction_time = time.time()
test_results = []
matched_directions = set()

# We'll test all 8 directions in random order
directions_to_test = directions.copy()
random.shuffle(directions_to_test)
current_direction_index = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img_h, img_w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # Draw safety margin rectangle
    margin = 80
    cv2.rectangle(frame, (margin, margin), (img_w - margin, img_h - margin), (0, 255, 0), 2)

    if not test_started:
        cv2.putText(frame, "Press 's' to start stroke gaze test", (30, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    else:
        if test_completed:
            # Calculate results
            correct_count = len(matched_directions)
            if correct_count == 8:
                result_text = "No abnormalities detected - All directions matched correctly"
                color = (0, 255, 0)
            else:
                result_text = f"Potential abnormalities detected - Matched {correct_count}/8 directions"
                color = (0, 0, 255)
            
            cv2.putText(frame, "Test Complete", (30, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, result_text, (30, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            cv2.imshow("Stroke Gaze Test", frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            continue
            
        if current_direction_index < len(directions_to_test):
            current_instruction = directions_to_test[current_direction_index]
            
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                mesh_points = np.array([(int(p.x * img_w), int(p.y * img_h)) 
                                     for p in face_landmarks.landmark])
                
                # Get landmarks for both eyes
                left_eye = mesh_points[LEFT_EYE_INDICES]
                right_eye = mesh_points[RIGHT_EYE_INDICES]
                left_iris = mesh_points[LEFT_IRIS_INDICES]
                right_iris = mesh_points[RIGHT_IRIS_INDICES]
                
                # Calculate gaze for both eyes
                left_x, left_y = get_gaze_ratio(left_eye, left_iris, frame.shape)
                right_x, right_y = get_gaze_ratio(right_eye, right_iris, frame.shape)
                
                # Average both eyes' gaze
                avg_x = (left_x + right_x) / 2
                avg_y = (left_y + right_y) / 2
                
                gaze_dir = determine_gaze_direction(avg_x, avg_y)
                
                # Check if gaze matches instruction
                if gaze_dir == current_instruction:
                    match_result = "Correct"
                    matched_directions.add(current_instruction)
                    current_direction_index += 1
                    last_instruction_time = time.time()
                else:
                    match_result = f"Look {current_instruction}"
                
                # Draw eye landmarks for visualization
                for point in left_eye:
                    cv2.circle(frame, tuple(point), 2, (0, 255, 0), -1)
                for point in left_iris:
                    cv2.circle(frame, tuple(point), 2, (0, 0, 255), -1)
        else:
            test_completed = True

        cv2.putText(frame, f"Instruction: {current_instruction}", (30, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if match_result:
            color = (0, 255, 0) if match_result == "Correct" else (0, 0, 255)
            cv2.putText(frame, match_result, (30, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Show progress
        progress = f"Progress: {len(matched_directions)}/8 directions matched"
        cv2.putText(frame, progress, (30, 130), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Stroke Gaze Test", frame)
    key = cv2.waitKey(5) & 0xFF
    if key == ord('s') and not test_started:
        test_started = True
        directions_to_test = directions.copy()
        random.shuffle(directions_to_test)
        current_direction_index = 0
        matched_directions = set()
        last_instruction_time = time.time()
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()