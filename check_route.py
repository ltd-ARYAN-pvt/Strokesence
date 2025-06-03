import requests
import numpy as np

def generate_dummy_data(label="stroke"):
    if label == "normal":
        accel = np.random.normal(0, 0.02, size=(300, 3)).tolist()
        gyro = np.random.normal(0, 0.01, size=(300, 3)).tolist()
    elif label == "elderly":
        accel = np.random.normal(0, 0.05, size=(300, 3)).tolist()
        gyro = np.random.normal(0, 0.03, size=(300, 3)).tolist()
    else:  # stroke
        accel = np.random.normal(0, 0.08, size=(300, 3)).tolist()
        gyro = np.random.normal(0, 0.06, size=(300, 3)).tolist()
    return {"accel": accel, "gyro": gyro}

# Change label to "normal", "elderly", or "stroke"
test_payload = generate_dummy_data(label="normal")
# print(test_payload)
response = requests.post("http://127.0.0.1:8000/analyze_balance", json=test_payload)
try:
    print("Test Result:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON. Status Code:", response.status_code)
    print("Response Text:", response.text)