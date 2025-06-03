import numpy as np

def analyze_balance(accel, gyro):
    # Path length
    path_length = np.sum(np.linalg.norm(np.diff(accel, axis=0), axis=1))

    # Sway area (approx bounding box)
    x, y = accel[:, 0], accel[:, 1]
    sway_area = (max(x) - min(x)) * (max(y) - min(y))

    # Angular velocity variance
    gyro_variance = np.var(gyro, axis=0).mean()

    # Jerkiness: derivative of acceleration
    jerk = np.diff(accel, axis=0)
    jerk_magnitude = np.linalg.norm(jerk, axis=1)
    jerkiness = np.mean(np.abs(jerk_magnitude))

    # threshold-based classification
    stroke_flag = (
        sway_area > 0.15 or 
        path_length > 15 or 
        gyro_variance > 0.002 or 
        jerkiness > 0.2
    )

    result = {
        "path_length": round(path_length, 2),
        "sway_area": round(sway_area, 2),
        "gyro_variance": round(gyro_variance, 5),
        "jerkiness": round(jerkiness, 5),
        "potential_stroke": bool(stroke_flag)
    }

    return result